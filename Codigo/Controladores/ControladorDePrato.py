from fastapi import HTTPException

from psycopg.rows import class_row, dict_row
from psycopg import connection

from Codigo.Controladores import ControladorDeTipo, ControladorDeCategoria
from Codigo.Entidades.Prato import Prato


@DeprecationWarning
def criar_instancia(prato: Prato, conn: connection):
    tipo = ControladorDeTipo.buscar_id(prato.get_tipo(), conn)
    categoria = ControladorDeCategoria.buscar_id(prato.get_categoria(), conn)
    return {
        "id": prato.get_id(),
        "nome": prato.get_nome(),
        "preco": prato.get_preco(),
        "categoria": categoria.get_nome(),
        "tipo": tipo.get_nome(),
        "quantidade_disponivel": prato.get_quantidade_disponivel()
    }


def listar_pratos(conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM prato_info ORDER BY id")
        return cur.fetchall()


def criar_prato(nome: str, preco: float, categoria: str, tipo: str, quantidade_disponivel: int, conn):
    tipo = ControladorDeTipo.buscar_tipo(tipo, conn)
    categoria = ControladorDeCategoria.buscar_categoria(categoria, conn)

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute(""
                    "INSERT INTO prato (nome, preco, categoria, tipo, quantidade_disponivel)"
                    "VALUES (%s, %s, %s, %s, %s) RETURNING *",
                    (nome, preco, categoria.get_id(), tipo.get_id()), quantidade_disponivel)
        return cur.fetchone()


def buscar_prato_por_nome(nome: str, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM prato_info WHERE nome = %s", (nome,))
        temp: Prato = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_prato_por_id(_id: int, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM prato_info WHERE id = %s", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_prato_por_categoria(categoria: str, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM prato_info WHERE categoria_nome = %s", (categoria,))
        return cur.fetchall()


def buscar_prato_por_tipo(tipo: str, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM prato_info WHERE tipo_nome = %s", (tipo,))
        return cur.fetchall()


def deletar_prato_por_id(_id: int, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("DELETE FROM prato_info WHERE id = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def alterar_informacao_prato(conn, prato_alvo_id: int = 0, nome: str = None, preco: float = None, categoria: str = None,
                             tipo: str = None):
    if prato_alvo_id == 0:
        raise HTTPException(status_code=422, detail="Invalid input for prato_id")

    prato_alvo = buscar_prato_por_id(prato_alvo_id, conn)
    tipo_original_id = prato_alvo.get("tipo")
    categoria_original_id = prato_alvo.get("categoria")

    if tipo is not None:
        tipo_alvo_id = ControladorDeTipo.buscar_tipo(tipo, conn).get_id()

    if categoria is not None:
        categoria_alvo_id = ControladorDeCategoria.buscar_categoria(categoria, conn).get_id()

    if prato_alvo is None:
        raise HTTPException(status_code=404)

    _nome = prato_alvo.get("nome") if nome is None else nome
    _preco = prato_alvo.get("preco") if preco is None else preco
    _categoria = categoria_original_id if categoria is None else categoria_alvo_id
    _tipo = tipo_original_id if tipo is None else tipo_alvo_id

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("UPDATE prato SET preco = %s, nome = %s, categoria = %s, tipo = %s "
                    "WHERE id = %s RETURNING *",
                    (_preco, _nome, _categoria, _tipo, prato_alvo_id))
        return cur.fetchone()
