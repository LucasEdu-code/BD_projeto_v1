from fastapi import HTTPException
from psycopg.rows import class_row
from psycopg import connection
from Codigo.Entidades.MetodoPagamento import MetodoPagamento


# Create
def criar(nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("INSERT INTO metodo_pagamento (nome) VALUES (%s) RETURNING *",
                    (nome, ))
        return cur.fetchone()


# READ
def buscar(id: int, conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("SELECT * FROM metodo_pagamento WHERE id = %s", (id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar_por_nome(nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("SELECT * FROM metodo_pagamento WHERE nome = %s", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def listar(conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("SELECT * FROM metodo_pagamento")
        return cur.fetchall()


# UPDATE
def mudar_nome(metodo_id, novo_nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("UPDATE metodo_pagamento SET nome = %s WHERE id = %s RETURNING *",
                    (novo_nome, metodo_id))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


# DELETE
def deletar(id: int, conn: connection):
    with conn.cursor(row_factory=class_row(MetodoPagamento)) as cur:
        cur.execute("DELETE FROM metodo_pagamento WHERE id = %s RETURNING *", (id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
