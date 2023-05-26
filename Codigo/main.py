import psycopg_pool

from Codigo.Controladores import ControladorDoHistorico, ControladorDeMesa, ControladorDePedido, ControladorDePrato

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_CONFIG = "dbname=postgres user=postgres password=123456789"

pool = psycopg_pool.ConnectionPool(conninfo=DB_CONFIG)

print("pool workers = {}".format(pool.num_workers))

tags_metadata = [
    {
        "name": "Mesa"
    },
    {
        "name": "Prato"
    },
    {
        "name": "Pedido"
    }
]

app = FastAPI(title="Restaurante API", openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MesaInfo(BaseModel):
    numero_integrantes: int | None = None
    pago: bool | None = None


class PratoInfo(BaseModel):
    nome: str | None = None
    preco: float | None = None
    categoria: str | None = None
    tipo: str | None = None


class PedidoInfo(BaseModel):
    id_mesa: int | None = None
    id_prato: int | None = None
    quantidade: int | None = None
    entregue: bool | None = None


# Mesa
@app.get("/mesas", tags=["Mesa"])
async def listar_mesas():
    with pool.connection() as conn:
        return ControladorDeMesa.listar_mesas(conn)


@app.get("/mesas/buscar/{mesa_id}", tags=["Mesa"])
async def buscar_mesa_por_id(mesa_id: int):
    with pool.connection() as conn:
        return ControladorDeMesa.buscar_mesa(mesa_id, conn)


@app.post("/mesas/criar", tags=["Mesa"])
async def criar_mesa(info: MesaInfo):
    with pool.connection() as conn:
        return ControladorDeMesa.criar_mesa(info.numero_integrantes, conn)


@app.put("/mesas/modificar/{mesa_id}", tags=["Mesa"])
async def modificar(mesa_id: int, info: MesaInfo):
    with pool.connection() as conn:
        if info.numero_integrantes is not None:
            ControladorDeMesa.alterar_numero_integrantes(mesa_id, info.numero_integrantes, conn)
        if info.pago is not None:
            ControladorDeMesa.atualizar_estado_pagamento(mesa_id, info.pago, conn)
        return ControladorDeMesa.buscar_mesa(mesa_id, conn)


@app.delete("/mesas/deletar/{mesa_id}", tags=["Mesa"])
async def deletar_mesa(mesa_id: int):
    with pool.connection() as conn:
        return ControladorDeMesa.deletar_mesa(mesa_id, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Prato
@app.get("/pratos", tags=["Prato"])
async def listar_todos_os_pratos():
    with pool.connection() as conn:
        return ControladorDePrato.listar_pratos(conn)


@app.get("/pratos/buscar/categoria/{nome}", tags=["Prato"])
async def buscar_prato_por_categoria(nome: str):
    with pool.connection() as conn:
        return ControladorDePrato.buscar_prato_por_categoria(nome, conn)


@app.get("/pratos/buscar/tipo/{nome}", tags=["Prato"])
async def buscar_prato_por_tipo(nome: str):
    with pool.connection() as conn:
        return ControladorDePrato.buscar_prato_por_tipo(nome, conn)


@app.get("/pratos/buscar/id/{prato_id}", tags=["Prato"])
async def buscar_prato_por_id(prato_id: int):
    with pool.connection() as conn:
        return ControladorDePrato.buscar_prato_por_id(prato_id, conn)


@app.get("/pratos/buscar/nome/{nome}", tags=["Prato"])
async def buscar_prato_por_nome(nome: str):
    with pool.connection() as conn:
        return ControladorDePrato.buscar_prato_por_nome(nome, conn)


@app.post("/pratos/criar", tags=["Prato"])
async def criar_prato(info: PratoInfo):
    with pool.connection() as conn:
        return ControladorDePrato.criar_prato(info.nome, info.preco, info.categoria, info.tipo, conn)


@app.put("/pratos/alterar/{prato_id}", tags=["Prato"])
async def alterar_informacoes_do_prato(prato_id: int, info: PratoInfo):
    with pool.connection() as conn:
        return ControladorDePrato.alterar_informacao_prato(conn, prato_id, info.nome, info.preco, info.categoria, info.tipo)


@app.delete("/pratos/deletar/{prato_id}", tags=["Prato"])
async def deletar_prato(prato_id: int):
    with pool.connection() as conn:
        return ControladorDePrato.deletar_prato_por_id(prato_id, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# pedido
@app.post("/pedidos/criar", tags=["Pedido"])
async def criar_pedido(info: PedidoInfo):
    with pool.connection() as conn:
        mesa = ControladorDeMesa.buscar_mesa(info.id_mesa, conn)
        prato = ControladorDePrato.buscar_prato_por_id(info.id_prato, conn)

    return ControladorDePedido.criar_pedido(prato, mesa, info.quantidade, conn)


@app.get("/pedidos", tags=["Pedido"])
async def listar_pedidos():
    with pool.connection() as conn:
        return ControladorDePedido.listar_pedidos(conn)


@app.get("/pedidos/buscar/id/{pedido_id}", tags=["Pedido"])
async def buscar_pedido_por_id(pedido_id: int):
    with pool.connection() as conn:
        return ControladorDePedido.buscar_pedido(pedido_id, conn)


@app.get("/pedidos/buscar/mesa/{mesa_id}", tags=["Pedido"])
async def listar_pedidos_por_mesa(mesa_id: int):
    with pool.connection() as conn:
        mesa = ControladorDeMesa.buscar_mesa(mesa_id, conn)
        return ControladorDePedido.listar_pedidos_por_mesa(mesa, conn)


@app.get("/pedidos/buscar/prato/{prato_id}", tags=["Pedido"])
async def listar_pedidos_por_prato(prato_id: int):
    with pool.connection() as conn:
        prato = ControladorDePrato.buscar_prato_por_id(prato_id, conn)
        return ControladorDePedido.listar_pedidos_por_prato(prato, conn)


@app.get("/pedidos/buscar/entregue/{estado}", tags=["Pedido"])
async def listar_pedidos_por_estado(estado: bool):
    with pool.connection() as conn:
        return ControladorDePedido.listar_pedidos_por_estado(estado, conn)


@app.put("/pedidos/modificar/{pedido_id}", tags=["Pedido"])
async def modificar(pedido_id: int, info: PedidoInfo):
    with pool.connection() as conn:
        return ControladorDePedido.modificar(pedido_id, info.entregue, info.id_prato, info.quantidade, conn)


@app.delete("/pedidos/deletar/{pedido_id}", tags=["Pedido"])
async def alterar_prato_do_pedido(pedido_id: int):
    with pool.connection() as conn:
        pedido = ControladorDePedido.buscar_pedido(pedido_id, conn)
        return ControladorDePedido.deletar_pedido(pedido, conn)


@app.put("/mesas/fechar/{mesa_id}", tags=["Fechar"])
async def fechar_mesa(mesa_id: int):
    with pool.connection() as conn:
        mesa = ControladorDeMesa.buscar_mesa(mesa_id, conn)
        if mesa.esta_pago():
            ControladorDePedido.salvar_pedidos(mesa, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Historico
@app.get("/historico/mesas", tags=["Historico_mesa"])
async def listar_historico_mesa():
    return ControladorDoHistorico.listar_mesa_historico()


@app.get("/historico/{historico_id}", tags=["Historico_mesa"])
async def buscar_historico_id_mesa(historico_id: int):
    return ControladorDoHistorico.buscar_mesa_historico_id(historico_id)


@app.get("/historico/mesas/{mesa_id}", tags=["Historico_mesa"])
async def buscar_historico_mesa_id(mesa_id: int):
    return ControladorDoHistorico.buscar_mesa_id_historico(mesa_id)


@app.get("/historico/pratos", tags=["Historico_prato"])
async def listar_historico_prato():
    return ControladorDoHistorico.listar_prato_historico()


@app.get("/historico/pratos/id/{prato_id}", tags=["Historico_prato"])
async def listar_historico_prato_id(prato_id: int):
    return ControladorDoHistorico.buscar_prato_id_historico(prato_id)


@app.get("/historico/pratos/nome/{nome}", tags=["Historico_prato"])
async def buscar_prato_nome_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_nome_historico(nome)


@app.get("/historico/pratos/tipo/{nome}", tags=["Historico_prato"])
async def buscar_prato_tipo_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_tipo_historico(nome)


@app.get("/historico/pratos/categoria/{nome}", tags=["Historico_prato"])
async def buscar_prato_categoria_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_categoria_historico(nome)


@app.get("/historico/pedidos", tags=["Historico_pedido"])
async def listar_pedidos_historico():
    return ControladorDoHistorico.listar_pedido_historico()


@app.get("/historico/pedidos/id/{pedido_id}", tags=["Historico_pedido"])
async def buscar_pedido_id_historico(pedido_id: int):
    return ControladorDoHistorico.buscar_pedido_id_historico(pedido_id)


@app.get("/historico/pedidos/mesa/{mesa_id}", tags=["Historico_pedido"])
async def buscar_pedidos_mesa_historico(mesa_id: int):
    return ControladorDoHistorico.buscar_pedidos_mesa_historico(mesa_id)


@app.get("/historico/pedidos/prato/{prato_id}", tags=["Historico_pedido"])
async def buscar_pedidos_prato_historico(prato_id: int):
    return ControladorDoHistorico.buscar_pedidos_prato_historico(prato_id)
