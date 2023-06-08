from fastapi import HTTPException

from psycopg.rows import class_row
from psycopg import connection

from Codigo.Controladores import ControladorDeTipo, ControladorDeCategoria
from Codigo.Entidades.Prato import Prato


# TODO Refatorar Tudo.

def criar_instancia(prato: Prato, conn: connection):
    tipo = ControladorDeTipo.buscar_id(prato.get_tipo(), conn)
    categoria = ControladorDeCategoria.buscar_id(prato.get_categoria(), conn)
    return {
        "id": prato.get_id(),
        "nome": prato.get_nome(),
        "preco": prato.get_preco(),
        "categoria": categoria.get_nome(),
        "tipo": tipo.get_nome()
    }


def listar_pratos(conn):
    retorno = []
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato ORDER BY id")
        for prato in cur.fetchall():
            retorno.append(criar_instancia(prato, conn))
        return retorno


def criar_prato(nome: str, preco: float, categoria: str, tipo: str, conn):
    tipo = ControladorDeTipo.buscar_tipo(tipo, conn)
    categoria = ControladorDeCategoria.buscar_categoria(categoria, conn)

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute(""
                    "INSERT INTO prato (nome, preco, categoria, tipo)"
                    "VALUES (%s, %s, %s, %s) RETURNING *",
                    (nome, preco, categoria.get_id(), tipo.get_id()))
        return cur.fetchone()


def buscar_prato_por_nome(nome: str, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE nome = %s", (nome,))
        temp: Prato = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return criar_instancia(temp, conn)


def buscar_prato_por_id(_id: int, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE id = %s", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return criar_instancia(temp, conn)


def buscar_prato_por_categoria(categoria: str, conn):
    retorno = []
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        categoria_id = ControladorDeCategoria.buscar_categoria(categoria, conn).get_id()
        cur.execute("SELECT * FROM prato WHERE categoria = %s", (categoria_id,))
        for prato in cur.fetchall():
            retorno.append(criar_instancia(prato, conn))
        return retorno


def buscar_prato_por_tipo(tipo: str, conn):
    retorno = []
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        tipo_id = ControladorDeTipo.buscar_tipo(tipo, conn).get_id()
        cur.execute("SELECT * FROM prato WHERE tipo = %s", (tipo_id,))
        for prato in cur.fetchall():
            retorno.append(criar_instancia(prato, conn))
        return retorno


def deletar_prato_por_id(_id: int, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("DELETE FROM prato WHERE id = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return criar_instancia(temp, conn)


def alterar_informacao_prato(conn, prato_alvo_id: int = 0, nome: str = None, preco: float = None, categoria: str = None,
                             tipo: str = None):
    if prato_alvo_id == 0:
        raise HTTPException(status_code=422, detail="Invalid input for prato_id")

    prato_alvo = buscar_prato_por_id(prato_alvo_id, conn)

    if prato_alvo is None:
        raise HTTPException(status_code=404)

    _nome = prato_alvo.get("nome") if nome is None else nome
    _preco = prato_alvo.get("preco") if preco is None else preco
    _categoria = prato_alvo.get("categoria") if categoria is None else categoria
    _tipo = prato_alvo.get("tipo") if tipo is None else tipo

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("UPDATE prato SET preco = %s, nome = %s, categoria = %s, tipo = %s "
                    "WHERE id = %s RETURNING *",
                    (_preco, _nome, _categoria, _tipo, prato_alvo_id))
        return cur.fetchone()
