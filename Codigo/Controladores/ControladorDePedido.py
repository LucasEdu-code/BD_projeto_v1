import datetime

from fastapi import HTTPException

from psycopg.rows import class_row

from Codigo.Controladores import ControladorDePrato, ControladorDeMesa
from Codigo.Entidades.Mesa import Mesa
from Codigo.Entidades.Prato import Prato
from Codigo.Relacoes.Pedido import Pedido


def criar_pedido(prato: Prato, mesa: Mesa, qnt: int, conn):
    with conn.cursor() as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                    (mesa.get_consumo_total(), mesa.get_id()))
        mesa.somar_ao_consumo(prato.get_preco() * qnt)

    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        date = datetime.datetime.now()
        cur.execute("INSERT INTO pedido (id_mesa, id_prato, quantidade, entregue, data)"
                    "VALUES (%s, %s, %s, %s, %s) RETURNING *",
                    (mesa.get_id(), prato.get_id(), qnt, False, date))

        return cur.fetchone()


def listar_pedidos(conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido")
        return cur.fetchall()


def buscar_pedido(_id: int, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE id_pedido = %s", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def listar_pedidos_por_mesa(mesa: Mesa, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE id_mesa = %s", (mesa.get_id(),))
        return cur.fetchall()


def listar_pedidos_por_prato(prato: Prato, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE id_prato = %s", (prato.get_id(),))
        return cur.fetchall()


def listar_pedidos_por_estado(entregue: bool, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE entregue = %s", (entregue,))
        return cur.fetchall()


def modificar(pedido_id: int, estado: bool, prato_novo_id: int, qnt: int, conn):
    if pedido_id == 0:
        raise HTTPException(status_code=422, detail="Invalid Input for pedido_id")

    pedido = buscar_pedido(pedido_id, conn)

    if estado is not None:
        _alterar_estado(pedido, estado, conn)
    if prato_novo_id is not None:
        _alterar_prato(pedido, prato_novo_id, conn)
    if qnt is not None:
        _alterar_quantidade(pedido, qnt, conn)

    return buscar_pedido(pedido_id, conn)


def _alterar_estado(pedido: Pedido, estado: bool, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("UPDATE pedido SET entregue = %s "
                    "WHERE id_pedido = %s RETURNING *",
                    (estado, pedido.get_id()))
        return cur.fetchone()


def _alterar_prato(pedido: Pedido, prato_novo_id: int, conn):
    prato_novo = ControladorDePrato.buscar_prato_por_id(prato_novo_id, conn)

    prato = ControladorDePrato.buscar_prato_por_id(pedido.get_prato_id(), conn)
    mesa = ControladorDeMesa.buscar_mesa(pedido.get_mesa_id(), conn)

    mesa.subtrair_do_consumo(prato.get_preco() * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato_novo.get_preco() * pedido.get_quantidade())

    with conn.cursor() as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                    (mesa.get_consumo_total(), pedido.get_mesa_id()))

    with conn.cursor(row_factory=class_row(Pedido)):
        cur.execute("UPDATE pedido SET id_prato = %s WHERE id_pedido = %s RETURNING *",
                    (prato_novo_id, pedido.get_id()))
        return cur.fetchone()


def _alterar_quantidade(pedido: Pedido, qnt: int, conn):
    mesa = ControladorDeMesa.buscar_mesa(pedido.get_mesa_id(), conn)
    prato = ControladorDePrato.buscar_prato_por_id(pedido.get_prato_id(), conn)

    mesa.subtrair_do_consumo(prato.get_preco() * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato.get_preco() * qnt)

    with conn.cursor() as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                    (mesa.get_consumo_total(), pedido.get_mesa_id()))

    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("UPDATE pedido SET quantidade = %s WHERE id_pedido = %s RETURNING *",
                    (qnt, pedido.get_id()))
        return cur.fetchone()


def deletar_pedido(pedido: Pedido, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("DELETE FROM pedido WHERE id_pedido = %s RETURNING *",
                    (pedido.get_id(),))
        pedido_removido = cur.fetchone()

    prato = ControladorDePrato.buscar_prato_por_id(pedido_removido.get_prato_id(), conn)
    mesa = ControladorDeMesa.buscar_mesa(pedido_removido.get_mesa_id(), conn)

    with conn.cursor() as cur:
        consumo = mesa.get_consumo_total() - (pedido_removido.quantidade * prato.get_preco())

        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id_mesa = %s",
                    (consumo, pedido_removido.get_mesa_id()))

    return pedido_removido


def salvar_pedidos(mesa: Mesa, conn):
    """
    Essa função ira remover todos os pedidos da mesa, e mové-los para o schema 'historico'.
    :param conn:
    :param mesa:
    :return None:
    """
    pedidos_fechados = listar_pedidos_por_mesa(mesa, conn)

    with conn.cursor(row_factory=class_row(Prato)) as cur:
        cur.execute("SELECT * from prato P, pedido PE WHERE P.id_prato = PE.id_prato")
        pratos = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute("INSERT INTO historico.mesa (id_mesa, numero_integrantes, consumo_total, pago) "
                    "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING data_insersao",
                    (mesa.get_id(), mesa.get_integrantes(), mesa.get_consumo_total(), mesa.esta_pago()))

        mesa_data = cur.fetchone()

        for prato in pratos:
            cur.execute("INSERT INTO historico.prato (id_prato, prato_nome, preco, prato_categoria, prato_tipo) "
                        "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (prato.get_id(), prato.get_nome(), prato.get_preco(), prato.get_categoria(), prato.get_tipo()))

        for pedido in pedidos_fechados:
            cur.execute("INSERT INTO historico.pedido "
                        "(id_pedido, id_mesa, id_prato, quantidade, entregue, data, data_mesa) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (pedido.get_id(), pedido.get_mesa_id(), pedido.get_prato_id(), pedido.get_quantidade(),
                         pedido.foi_entregue(), pedido.get_datetime(), mesa_data))

        cur.execute("DELETE FROM pedido WHERE id_mesa = %s", (mesa.get_id(),))
        cur.execute("UPDATE mesa SET pago = false, consumo_total = 0 WHERE id_mesa = %s", (mesa.get_id(),))
