import datetime

from fastapi import HTTPException

from psycopg.rows import class_row, dict_row

from Codigo.Controladores import ControladorDePrato, ControladorDeMesa
from Codigo.Entidades.Mesa import Mesa
from Codigo.Entidades.Prato import Prato
from Codigo.Relacoes.Pedido import Pedido
from psycopg import connection


def listar_pedidos_com_view(conn: connection):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM pedido_info")
        return cur.fetchall()


def buscar_por_periodo(inicio: str, fim: str, conn: connection):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM pedido_info WHERE data > %s AND data < %s", (inicio, fim))
        return cur.fetchall()


def quantidade(conn: connection):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(id_pedido) FROM pedido")
        return cur.fetchone()


def custo_total(conn: connection):
    total = 0
    with conn.cursor() as cur:
        for pedido in listar_pedidos(conn):
            total += pedido.get("prato_preco") * pedido.get("quantidade")
        return total


def criar_pedido(prato, mesa: Mesa, qnt: int, conn):
    if prato.get("quantidade_disponivel") <= 0:
        raise HTTPException(status_code=405, detail="Produto em falta no estoque.")

    mesa.somar_ao_consumo(prato.get("preco") * qnt)
    with conn.cursor() as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id = %s",
                    (mesa.get_consumo_total(), mesa.get_id()))
        cur.execute("UPDATE prato SET quantidade_disponivel = %s WHERE id = %s",
                    (prato.get("quantidade_disponivel") - qnt, prato.get("id")))

    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        date = datetime.datetime.now()
        cur.execute("INSERT INTO pedido (id_mesa, id_prato, quantidade, entregue, data)"
                    "VALUES (%s, %s, %s, %s, %s) RETURNING *",
                    (mesa.get_id(), prato.get("id"), qnt, False, date))

        return cur.fetchone()


def listar_pedidos(conn):
    tempo = []
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido ORDER BY id_pedido")
        pedidos = cur.fetchall()

    for pedido in pedidos:
        with conn.cursor() as cur:
            cur.execute("SELECT nome, preco from prato where id = %s", (pedido.get_prato_id(),))
            prato = cur.fetchone()
            temp = {
                "id_pedido": pedido.get_id(),
                "id_mesa": pedido.get_mesa_id(),
                "id_prato": pedido.get_prato_id(),
                "prato_nome": prato[0],
                "prato_preco": prato[1],
                "quantidade": pedido.get_quantidade(),
                "entregue": pedido.foi_entregue(),
                "data": pedido.get_datetime()
            }
            tempo.append(temp)

    return tempo


def _buscar_pedido(_id: int, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE id_pedido = %s", (_id,))
        pedido = cur.fetchone()

        if pedido is None:
            raise HTTPException(status_code=404)

        return pedido


def buscar_pedido(_id: int, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("SELECT * from pedido WHERE id_pedido = %s", (_id,))
        pedido = cur.fetchone()

    if pedido is None:
        raise HTTPException(status_code=404)

    with conn.cursor() as cur:
        cur.execute("SELECT nome, preco from prato where id = %s", (pedido.get_prato_id(),))
        prato = cur.fetchone()

    temp = {
        "id_pedido": pedido.get_id(),
        "id_mesa": pedido.get_mesa_id(),
        "id_prato": pedido.get_prato_id(),
        "prato_nome": prato[0],
        "prato_preco": prato[1],
        "quantidade": pedido.get_quantidade(),
        "entregue": pedido.foi_entregue(),
        "data": pedido.get_datetime()
    }

    return temp


def listar_pedidos_por_mesa(mesa: Mesa, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * from pedido_info WHERE id_mesa = %s", (mesa.get_id(),))
        return cur.fetchall()


def listar_pedidos_por_prato(prato, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * from pedido_info WHERE id_prato = %s", (prato.get("id"),))
        return cur.fetchall()


def listar_pedidos_por_categoria(categoria_id: int, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * from pedido_info WHERE categoria = %s", (categoria_id,))
        return cur.fetchall()


def listar_pedidos_por_tipo(tipo_id: int, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * from pedido_info WHERE tipo = %s", (tipo_id,))
        return cur.fetchall()


def listar_pedidos_por_estado(entregue: bool, conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * from pedido_info WHERE entregue = %s", (entregue,))
        return cur.fetchall()


def modificar(pedido_id: int, estado: bool, prato_novo_id: int, qnt: int, conn):
    if pedido_id == 0:
        raise HTTPException(status_code=422, detail="Invalid Input for pedido_id")

    pedido = _buscar_pedido(pedido_id, conn)

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

    mesa.subtrair_do_consumo(prato.get("preco") * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato_novo.get("preco") * pedido.get_quantidade())

    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id = %s",
                    (mesa.get_consumo_total(), pedido.get_mesa_id()))

        cur.execute("UPDATE pedido SET id_prato = %s WHERE id_pedido = %s RETURNING *",
                    (prato_novo_id, pedido.id_pedido))
        return cur.fetchone()


def _alterar_quantidade(pedido: Pedido, qnt: int, conn):
    mesa = ControladorDeMesa.buscar_mesa(pedido.get_mesa_id(), conn)
    prato = ControladorDePrato.buscar_prato_por_id(pedido.get_prato_id(), conn)

    mesa.subtrair_do_consumo(prato.get("preco") * pedido.get_quantidade())
    mesa.somar_ao_consumo(prato.get("preco") * qnt)

    with conn.cursor() as cur:
        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id = %s",
                    (mesa.get_consumo_total(), pedido.get_mesa_id()))

    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("UPDATE pedido SET quantidade = %s WHERE id_pedido = %s RETURNING *",
                    (qnt, pedido.get_id()))
        return cur.fetchone()


def deletar_pedido(pedido: Pedido, conn):
    with conn.cursor(row_factory=class_row(Pedido)) as cur:
        cur.execute("DELETE FROM pedido WHERE id_pedido = %s RETURNING *",
                    (pedido.id_pedido,))
        pedido_removido = cur.fetchone()

    prato = ControladorDePrato.buscar_prato_por_id(pedido_removido.get_prato_id(), conn)
    mesa = ControladorDeMesa.buscar_mesa(pedido_removido.get_mesa_id(), conn)

    with conn.cursor() as cur:
        consumo = mesa.get_consumo_total() - (pedido_removido.quantidade * prato.get("preco"))

        cur.execute("UPDATE mesa SET consumo_total = %s WHERE id = %s",
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
        cur.execute("SELECT * from prato P, pedido PE WHERE P.id = PE.id_prato")
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
        cur.execute("UPDATE mesa SET pago = false, consumo_total = 0 WHERE id = %s", (mesa.get_id(),))
