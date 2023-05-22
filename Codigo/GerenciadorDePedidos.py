import datetime
import psycopg

from psycopg.types import none
from psycopg.rows import class_row

from Entidades.Mesa import Mesa
from Entidades.Prato import Prato
from Relacoes.Pedido import Pedido

DB_CONFIG = "dbname=postgres user=postgres password=123456789"


# MESA
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


# PRATO
def criar_prato(nome: str, preco: float, categoria: str, tipo: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute(""
                        "INSERT INTO prato (prato_nome, preco, prato_categoria, prato_tipo)"
                        "VALUES (%s, %s, %s, %s) RETURNING *",
                        (nome, preco, categoria, tipo))
            return cur.fetchone()


def listar_pratos():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato")
            return cur.fetchall()


def buscar_prato_por_nome(nome: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_nome = %s", (nome,))
            return cur.fetchall()


def buscar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE id_prato = %s", (_id,))
            return cur.fetchone()


def buscar_prato_por_categoria(categoria: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_categoria = %s", (categoria,))
            return cur.fetchall()


def buscar_prato_por_tipo(tipo: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_tipo = %s", (tipo,))
            return cur.fetchall()


def deletar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("DELETE FROM prato WHERE id_prato = %s RETURNING *", (_id,))
            return cur.fetchone()


def alterar_informacao_prato(prato_alvo_id: int = 0, nome: str = "", preco: float = 0, categoria: str = "",
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
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                        "WHERE id_prato = %s RETURNING *",
                        (preco, nome, categoria, tipo, prato_alvo_id))
            return cur.fetchone()


# Pedido
def criar_pedido(prato: Prato, mesa: Mesa, qnt: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT EXISTS (SELECT 1 from mesa WHERE id_mesa = %s)", (mesa.get_id(),))
            if cur.fetchone() == none:
                return none

            cur.execute("SELECT EXISTS (SELECT 1 from prato WHERE id_prato = %s)", (prato.get_id(),))
            if cur.fetchone() == none:
                return none

            mesa.somar_ao_consumo(prato.get_preco() * qnt)
            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (mesa.get_consumo_total(), mesa.get_id()))

        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            date = datetime.datetime.now()
            cur.execute("INSERT INTO pedido (id_mesa, id_prato, quantidade, entregue, data)"
                        "VALUES (%s, %s, %s, %s, %s) RETURNING *",
                        (mesa.get_id(), prato.get_id(), qnt, False, date))

            return cur.fetchone()


def listar_pedidos():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from pedido")
            return cur.fetchall()


def buscar_pedido(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from pedido WHERE id_pedido = %s", (_id,))
            return cur.fetchone()


def listar_pedidos_por_mesa(mesa_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from pedido WHERE id_mesa = %s", (mesa_id,))
            cur.fetchall()


def listar_pedidos_por_prato(prado_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from pedido WHERE id_prato = %s", (prado_id,))
            return cur.fetchall()


def listar_pedidos_por_estado(entregue: bool):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from pedido WHERE entregue = %s", (entregue,))
            return cur.fetchall()


def alterar_estado_do_pedido(pedido_id: int, estado: bool):
    if pedido_id == 0:
        return none
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("UPDATE pedido SET entregue = %s "
                        "WHERE id_pedido = %s RETURNING *",
                        (estado, pedido_id))
            return cur.fetchone()


def alterar_prato_do_pedido(pedido_id: int, prato_novo_id: int):
    pedido = buscar_pedido(pedido_id)
    prato_novo = buscar_prato_por_id(prato_novo_id)

    if pedido == none or prato_novo == none:
        return none

    prato = buscar_prato_por_id(pedido.get_prato_id())
    mesa = buscar_mesa(pedido.get_mesa_id())

    mesa.subtrair_do_consumo(prato.get_preco() * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato_novo.get_preco() * pedido.get_quantidade())

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (mesa.get_consumo_total(), pedido.get_mesa_id()))

        with conn.cursor(row_factory=class_row(Pedido)):
            cur.execute("UPDATE pedido SET id_prato = %s WHERE id_pedido = %s RETURNING *",
                        (prato_novo_id, pedido_id))
            return cur.fetchone()


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
            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (mesa.get_consumo_total(), pedido.get_mesa_id()))

        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("UPDATE pedido SET quantidade = %s WHERE id_pedido = %s RETURNING *",
                        (qnt, pedido_id))
            return cur.fetchone()


def deletar_pedido(pedido_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("DELETE FROM pedido WHERE id_pedido = %s RETURNING *",
                        (pedido_id,))
            pedido_removido = cur.fetchone()

        with conn.cursor() as cur:
            consumo = cur.execute("SELECT consumo_total FROM mesa WHERE id_mesa = %s",
                                  (pedido_removido.get_mesa_id(),)).fetchone()[0]
            prato = \
            cur.execute("SELECT preco FROM prato WHERE id_prato = %s", (pedido_removido.get_prato_id(),)).fetchone()[0]
            consumo -= pedido_removido.quantidade * prato

            cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                        (consumo, pedido_removido.get_mesa_id()))

        return pedido_removido


# FUNÇÕES PARA O HISTÓRICO
def fechar_mesa(mesa_id):
    """
    Essa função ira remover todos os pedidos da mesa, e move-los para o schema 'historico'.
    :param mesa_id:
    :return None:
    """

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * from mesa WHERE id_mesa = %s", (mesa_id,))
            mesa_fechada = cur.fetchone()

            cur.execute("SELECT * from pedido WHERE id_mesa = %s", (mesa_id,))
            pedidos_fechados = cur.fetchall()

            cur.execute("SELECT * from prato P, pedido PE WHERE P.id_prato = PE.id_prato")
            pratos = cur.fetchall()

            cur.execute("INSERT INTO historico.mesa (id_mesa, numero_integrantes, consumo_total, pago) "
                        "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (mesa_fechada[0], mesa_fechada[1], mesa_fechada[2], mesa_fechada[3]))

            for prato in pratos:
                cur.execute("INSERT INTO historico.prato (id_prato, prato_nome, preco, prato_categoria, prato_tipo) "
                            "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                            (prato[0], prato[1], prato[2], prato[3], prato[4]))

            for pedido in pedidos_fechados:
                cur.execute("INSERT INTO historico.pedido (id_pedido, id_mesa, id_prato, quantidade, entregue, data) "
                            "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                            (pedido[0], pedido[1], pedido[2], pedido[3], pedido[4], pedido[5]))

            cur.execute("DELETE FROM pedido WHERE id_mesa = %s", (mesa_id,))
            cur.execute("UPDATE mesa SET pago = false, consumo_total = 0 WHERE id_mesa = %s", (mesa_id,))
