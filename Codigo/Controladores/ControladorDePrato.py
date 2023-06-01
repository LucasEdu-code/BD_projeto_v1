from fastapi import HTTPException

from psycopg.rows import class_row
from Codigo.Entidades.Prato import Prato


def listar_pratos(conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato ORDER BY id_prato ASC")
        return cur.fetchall()


def criar_prato(nome: str, preco: float, categoria: str, tipo: str, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute(""
                    "INSERT INTO prato (prato_nome, preco, prato_categoria, prato_tipo)"
                    "VALUES (%s, %s, %s, %s) RETURNING *",
                    (nome, preco, categoria, tipo))
        return cur.fetchone()


def buscar_prato_por_nome(nome: str, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE prato_nome = %s", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_prato_por_id(_id: int, conn) -> Prato:
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE id_prato = %s", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_prato_por_categoria(categoria: str, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE prato_categoria = %s", (categoria,))
        return cur.fetchall()


def buscar_prato_por_tipo(tipo: str, conn):
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * FROM prato WHERE prato_tipo = %s", (tipo,))
        return cur.fetchall()


def deletar_prato_por_id(_id: int, conn) -> Prato:
    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("DELETE FROM prato WHERE id_prato = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def alterar_informacao_prato(conn, prato_alvo_id: int = 0, nome: str = None, preco: float = None, categoria: str = None,
                             tipo: str = None):
    if prato_alvo_id == 0:
        raise HTTPException(status_code=422, detail="Invalid input for prato_id")

    prato_alvo = buscar_prato_por_id(prato_alvo_id, conn)

    if prato_alvo is None:
        raise HTTPException(status_code=404)

    _nome = prato_alvo.get_nome() if nome is None else nome
    _preco = prato_alvo.get_preco() if preco is None else preco
    _categoria = prato_alvo.get_categoria() if categoria is None else categoria
    _tipo = prato_alvo.get_tipo() if tipo is None else tipo

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                    "WHERE id_prato = %s RETURNING *",
                    (_preco, _nome, _categoria, _tipo, prato_alvo_id))
        return cur.fetchone()
