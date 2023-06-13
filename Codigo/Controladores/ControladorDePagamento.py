from fastapi import HTTPException, status, Response
from psycopg.rows import class_row, dict_row
from psycopg import connection

from Codigo.Controladores import ControladorDeCliente, ControladorDeMesa, ControladorDeMetodoPagamento
from Codigo.Relacoes.Pagamento import Pagamento


def efetuar_pagamento(cliente_id: int, mesa_id: int, metodo_id: int, conn: connection):
    cliente = ControladorDeCliente.buscar(cliente_id, conn)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    mesa = ControladorDeMesa.buscar_mesa(mesa_id, conn)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa não encontrada.")
    metodo = ControladorDeMetodoPagamento.buscar(metodo_id, conn)
    if metodo is None:
        raise HTTPException(status_code=404, detail="Metodo Não encontrado.")

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("CALL efetuar_pagamento(%s, %s, %s)", (cliente_id, mesa_id, metodo_id))


def listar(cliente_id: int, conn):
    cliente = ControladorDeCliente.buscar(cliente_id, conn)

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM pagamento_info WHERE cliente_nome = %s", (cliente.nome, ))
        return cur.fetchall()
