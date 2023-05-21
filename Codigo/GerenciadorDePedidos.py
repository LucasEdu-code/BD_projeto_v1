import datetime

from psycopg.types import none

from Entidades.Prato import Prato
from Entidades.Mesa import Mesa
from Relacoes.Pedido import Pedido

import psycopg

DB_CONFIG = "dbname=postgres user=postgres password=123456789"


# MESA
def criar_mesa(numero_integrantes: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO mesa (numero_integrantes, consumo_total, pago) "
                        "VALUES (%s, %s, %s)",
                        (numero_integrantes, 0.0, False))


def listar_mesas():
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mesa")
            for mesa in cur.fetchall():
                lista.append(Mesa(mesa[0], mesa[1], mesa[2], mesa[3]))
            return lista


def buscar_mesa(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mesa WHERE id_mesa = %s", (_id,))
            _temp = cur.fetchone()
            return Mesa(_temp[0], _temp[1], _temp[2], _temp[3])


def deletar_mesa(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM mesa WHERE id_mesa = {} RETURNING *".format(_id))
            delete_value = cur.fetchone()
            return Mesa(delete_value[0], delete_value[1], delete_value[2], delete_value[3])


def alterar_numero_integrantes(mesa_id: int, numero_integrantes: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE mesa SET numero_integrantes = %s WHERE id_mesa = %s", (numero_integrantes, mesa_id))


def atualizar_consumo(_id: int):
    # TODO implementar depois a tabela da relação, pedido.
    pass


def atualizar_estado_pagamento(mesa_id: int, estado: bool):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE mesa SET pago = %s WHERE id_mesa = %s", (estado, mesa_id))


# PRATO
def criar_prato(nome: str, preco: float, categoria: str, tipo: str):
    return Prato(0, nome, preco, categoria, tipo)


def enviar_prato(prato: Prato):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(""
                        "INSERT INTO prato ( preco, prato_nome, prato_categoria, prato_tipo)"
                        "VALUES (%s, %s, %s, %s)",
                        (prato.get_preco(), prato.get_nome(), prato.get_categoria(), prato.get_tipo()))


def listar_pratos():
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato")
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_nome(nome: str):
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE prato_nome = '{}'".format(nome))
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE id_prato = {}".format(_id))
            prato = cur.fetchone()
            return Prato(prato[0], prato[2], prato[1], prato[3], prato[4])


def deletar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
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

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                        "WHERE id_prato = %s",
                        (preco, nome, categoria, tipo, prato_alvo_id))


# Pedido
def criar_pedido(prato: Prato, mesa: Mesa, qnt: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            mesa = buscar_mesa(mesa.mesa_id())
            if none:
                return none

            cur.execute("SELECT EXISTS (SELECT 1 from prato WHERE id_prato = %s)", (prato.get_id(),))
            if not cur.fetchone():
                return none

            date = datetime.datetime.now()
            cur.execute("INSERT INTO pedido (id_mesa, id_prato, quantidade, entregue, data)"
                        "VALUES (%s, %s, %s, %s, %s) RETURNING *",
                        (mesa.mesa_id(), prato.get_id(), qnt, False, date))
            temp = cur.fetchone()
            pedido_feito = Pedido(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])

            mesa.somar_ao_consumo(prato.get_preco()*qnt)

            return pedido_feito


def listar_pedidos():
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from pedido")
            for pedido in cur.fetchall():
                lista.append(Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]))
            return lista


def buscar_pedido(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from pedido WHERE id_pedido = %s", (_id,))
            pedido = cur.fetchone()
            return Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5])


def listar_pedidos_por_mesa(mesa_id: int):
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from pedido WHERE id_mesa = %s", (mesa_id,))
            for pedido in cur.fetchall():
                lista.append(Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]))
            return lista


def listar_pedidos_por_prato(prado_id: int):
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from pedido WHERE id_prato = %s", (prado_id,))
            for pedido in cur.fetchall():
                lista.append(Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]))
            return lista


def listar_pedidos_por_estado(entregue: bool):
    lista = []
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from pedido WHERE entregue = %s", (entregue,))
            for pedido in cur.fetchall():
                lista.append(Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]))
            return lista


def alterar_estado_do_pedido(pedido_id: int, estado: bool):
    if pedido_id == 0:
        return none
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET entregue = %s "
                        "WHERE id_pedido = %s",
                        (estado, pedido_id))


def alterar_prato_do_pedido(pedido_id: int, prato_novo_id: int):
    pedido = buscar_pedido(pedido_id)
    prato_novo = buscar_prato_por_id(prato_novo_id)

    if pedido == none or prato_novo == none:
        return none

    prato = buscar_prato_por_id(pedido.get_prato_id())
    mesa = buscar_mesa(pedido.get_mesa_id())

    mesa.subtrair_do_consumo(prato.get_preco()*pedido.get_quantidade())
    mesa.somar_ao_consumo(prato_novo.get_preco()*pedido.get_quantidade())

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET id_prato = %s WHERE id_pedido = %s RETURNING *",
                        (prato_novo_id, pedido_id))
            pedido_atualizado = cur.fetchone()

            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (mesa.consumo_total(), pedido.get_mesa_id()))

            return pedido_atualizado


def alterar_quantidade_do_pedido(pedido_id: int, qnt: int):
    pedido = buscar_pedido(pedido_id)

    if pedido == none:
        return none

    mesa = buscar_mesa(pedido.get_mesa_id())
    prato = buscar_prato_por_id(pedido.get_prato_id())

    mesa.subtrair_do_consumo(prato.get_preco() * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato.get_preco() * qnt)

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET quantidade = %s WHERE id_pedido = %s RETURNING *",
                        (qnt, pedido_id))
            pedido_atualizado = cur.fetchone()

            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (mesa.consumo_total(), pedido.get_mesa_id()))

            return pedido_atualizado


def deletar_pedido(pedido_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pedido WHERE id_pedido = %s RETURNING *",
                        (pedido_id,))
            pedido = cur.fetchone()
            return Pedido(pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5])
