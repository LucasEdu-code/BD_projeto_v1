import psycopg

from psycopg.rows import class_row
from Codigo.Entidades.Mesa import Mesa

DB_CONFIG = "dbname=projeto user=postgres password=622644le"

def criar_mesa(numero_integrantes: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("INSERT INTO mesa (numero_integrantes, consumo_total, pago) "
                        "VALUES (%s, %s, %s) RETURNING *",
                        (numero_integrantes, 0.0, False))
            return cur.fetchone()


def listar_mesas():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("SELECT * FROM mesa ORDER BY id_mesa ASC")
            return cur.fetchall()


def buscar_mesa(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("SELECT * FROM mesa WHERE id_mesa = %s", (_id,))
            return cur.fetchone()


def deletar_mesa(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("DELETE FROM mesa WHERE id_mesa = %s RETURNING *", (_id,))
            return cur.fetchone()


def alterar_numero_integrantes(mesa_id: int, numero_integrantes: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("UPDATE mesa SET numero_integrantes = %s WHERE id_mesa = %s RETURNING *",
                        (numero_integrantes, mesa_id))
            return cur.fetchone()
        
def atualizar_consumo(_id: int):
    # TODO implementar depois a tabela da relação, pedido.
    pass
        
def atualizar_estado_pagamento(mesa_id: int, estado: bool):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("UPDATE mesa SET pago = %s WHERE id_mesa = %s RETURNING *",
                        (estado, mesa_id))
            return cur.fetchone()
        
