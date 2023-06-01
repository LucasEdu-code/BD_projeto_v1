from psycopg import connection
from psycopg.rows import class_row
from Codigo.Entidades.Categoria import Categoria
from fastapi import HTTPException


def criar_categoria(nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(Categoria)) as cur:
        cur.execute("INSERT INTO categoria (nome) VALUES (%s) RETURNING *", (nome,))
        return cur.fetchone()


def listar_categorias(conn: connection):
    with conn.cursor(row_factory=class_row(Categoria)) as cur:
        cur.execute("SELECT * FROM categoria ORDER BY id")
        return cur.fetchall()


def buscar_categoria(nome: str, conn: connection) -> Categoria:
    with conn.cursor(row_factory=class_row(Categoria)) as cur:
        cur.execute("SELECT * FROM categoria WHERE nome = %s", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def deletar_categoria(nome: str, conn: connection) -> Categoria:
    with conn.cursor(row_factory=class_row(Categoria)) as cur:
        cur.execute("DELETE FROM categoria WHERE nome = %s RETURNING *", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def alterar_nome(nome_antigo: str, nome_novo: str, conn: connection) -> Categoria:
    with conn.cursor(row_factory=class_row(Categoria)) as cur:
        cur.execute("UPDATE categoria SET nome = %s WHERE nome = %s RETURNING *",
                    (nome_novo, nome_antigo))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
