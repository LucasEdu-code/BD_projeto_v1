from Entidades.Prato import Prato
from Entidades.Mesa import Mesa
import psycopg


# MESA
def criar_mesa(numero_integrantes: int):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO mesa (numero_integrantes, consumo_total, pago) "
                        "VALUES (%s, %s, %s)",
                        (numero_integrantes, 0.0, False))


def listar_mesas():
    lista = []
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mesa")
            for mesa in cur.fetchall():
                lista.append(Mesa(mesa[0], mesa[1], mesa[2], mesa[3]))
            return lista


def buscar_mesa(_id: int):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mesa WHERE id_mesa = %s", (_id,))
            _temp = cur.fetchone()
            return Mesa(_temp[0], _temp[1], _temp[2], _temp[3])


def deletar_mesa(_id: int):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM mesa WHERE id_mesa = {} RETURNING *".format(_id))
            delete_value = cur.fetchone()
            return Mesa(delete_value[0], delete_value[1], delete_value[2], delete_value[3])


def alterar_numero_integrantes(mesa_id: int, numero_integrantes: int):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE mesa SET numero_integrantes = %s WHERE id_mesa = %s", (numero_integrantes, mesa_id))


def atualizar_consumo(_id: int):
    # TODO implementar depois a tabela da relação, pedido.
    pass


def atualizar_estado_pagamento(mesa_id: int, estado: bool):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE mesa SET pago = %s WHERE id_mesa = %s", (estado, mesa_id))


# PRATO
def criar_prato(nome: str, preco: float, categoria: str, tipo: str):
    return Prato(0, nome, preco, categoria, tipo)


def enviar_prato(prato: Prato):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute(""
                        "INSERT INTO prato ( preco, prato_nome, prato_categoria, prato_tipo)"
                        "VALUES (%s, %s, %s, %s)"
                        , (prato.get_preco(), prato.get_nome(), prato.get_categoria(), prato.get_tipo()))


def listar_pratos():
    lista = []
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato")
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_nome(nome: str):
    lista = []
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE prato_nome = '{}'".format(nome))
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE id_prato = {}".format(_id))
            prato = cur.fetchone()
            return Prato(prato[0], prato[2], prato[1], prato[3], prato[4])


def deletar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM prato WHERE id_prato = {} RETURNING *".format(_id))
            delete_value = cur.fetchone()
            return Prato(delete_value[0], delete_value[2], delete_value[1], delete_value[3], delete_value[4])


def alterar_valores_prato(prato_alvo_id: int = 0, nome: str = "", preco: float = 0, categoria: str = "",
                          tipo: str = ""):
    if prato_alvo_id == 0:
        return

    prato_alvo = buscar_prato_por_id(prato_alvo_id)

    if nome == "":
        nome = prato_alvo.get_nome()

    if preco == 0:
        preco = prato_alvo.get_preco()

    if categoria == "":
        categoria = prato_alvo.get_categoria()

    if tipo == "":
        tipo = prato_alvo.get_tipo()

    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                        "WHERE id_prato = %s"
                        , (preco, nome, categoria, tipo, prato_alvo_id))
