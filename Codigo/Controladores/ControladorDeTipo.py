from psycopg import connection
from psycopg.rows import class_row
from Codigo.Entidades.Tipo import Tipo
from fastapi import HTTPException


def criar_tipo(nome: str, conn: connection) -> Tipo:
    if nome is None:
        raise HTTPException(status_code=422)

    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("INSERT INTO tipo (nome) VALUES (%s) RETURNING *",
                    (nome,))
        return cur.fetchone()


def listar_tipos(conn: connection):
    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("SELECT * FROM tipo ORDER BY id")
        return cur.fetchall()


def buscar_tipo(nome: str, conn: connection) -> Tipo:
    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("SELECT * FROM tipo WHERE nome = %s", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_id(_id: int, conn: connection) -> Tipo:
    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("SELECT * FROM tipo WHERE id = %s", (_id,))
        return cur.fetchone()


def deletar_tipo(_id: int, conn: connection) -> Tipo:
    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("DELETE FROM tipo WHERE id = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def alterar_nome(nome_antigo: str, nome_novo: str, conn: connection) -> Tipo:
    with conn.cursor(row_factory=class_row(Tipo)) as cur:
        cur.execute("UPDATE tipo SET nome = %s WHERE nome = %s RETURNING *",
                    (nome_novo, nome_antigo))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
