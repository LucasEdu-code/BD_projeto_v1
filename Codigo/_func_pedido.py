import datetime
import psycopg

from psycopg.types import none
from psycopg.rows import class_row

from Codigo.Relacoes.Pedido import Pedido
from Codigo.Entidades.Mesa import Mesa
from Codigo.Entidades.Prato import Prato

import Codigo._func_mesa as F_mesa
import Codigo._func_prato as F_prato

DB_CONFIG = "dbname=projeto user=postgres password=622644le"

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
    prato_novo = F_prato.buscar_prato_por_id(prato_novo_id)

    if pedido == none or prato_novo == none:
        return none

    prato = F_prato.buscar_prato_por_id(pedido.get_prato_id())
    mesa = F_mesa.buscar_mesa(pedido.get_mesa_id())

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

    mesa = F_mesa.buscar_mesa(pedido.get_mesa_id())
    prato = F_prato.buscar_prato_por_id(pedido.get_prato_id())

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
    
 
def salvar_pedidos(mesa_id):
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
