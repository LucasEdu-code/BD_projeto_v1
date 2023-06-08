from fastapi import HTTPException
from psycopg.rows import class_row
from Codigo.Entidades.Mesa import Mesa


def listar_mesas(conn):
    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("SELECT * FROM mesa ORDER BY id")
        return cur.fetchall()


def buscar_mesa(_id: int, conn):
    if _id == 0:
        raise HTTPException(status_code=422)

    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("SELECT * FROM mesa WHERE id = %s", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def criar_mesa(numero_integrantes: int, conn):
    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("INSERT INTO mesa (numero_integrantes, consumo_total, pago) "
                    "VALUES (%s, %s, %s) RETURNING *",
                    (numero_integrantes, 0.0, False))
        return cur.fetchone()


def deletar_mesa(_id: int, conn):
    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("DELETE FROM mesa WHERE id = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def alterar_numero_integrantes(mesa_id: int, numero_integrantes: int, conn):
    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("UPDATE mesa SET numero_integrantes = %s WHERE id = %s RETURNING *",
                    (numero_integrantes, mesa_id))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def atualizar_estado_pagamento(mesa_id: int, estado: bool, conn):
    with conn.cursor(row_factory=class_row(Mesa)) as cur:
        cur.execute("UPDATE mesa SET pago = %s WHERE id = %s RETURNING *",
                    (estado, mesa_id))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
