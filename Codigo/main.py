import GerenciadorDePedidos as GP
from fastapi import FastAPI
from pydantic import BaseModel

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


class MesaInfo(BaseModel):
    numero_integrantes: int | None = None
    pago: bool | None = None


class PratoInfo(BaseModel):
    nome: str | None = ""
    preco: float | None = 0
    categoria: str | None = ""
    tipo: str | None = ""


class PedidoInfo(BaseModel):
    id_mesa: int
    id_prato: int
    quantidade: int
    entregue: bool | None = False


class PedidoAlterado(BaseModel):
    id_prato: int | None = 0
    quantidade: int | None = 0
    entregue: bool | None = False


# Mesa
@app.get("/mesas", tags=["Mesa"])
async def listar_mesas():
    return GP.listar_mesas()


@app.post("/mesas/criar", tags=["Mesa"])
async def criar_mesa(info: MesaInfo):
    return GP.criar_mesa(info.numero_integrantes)


@app.delete("/mesas/deletar/{mesa_id}", tags=["Mesa"])
async def deletar_mesa(mesa_id: int):
    return GP.deletar_mesa(mesa_id)


@app.put("/mesas/{mesa_id}/alterar-qnt-integrantes", tags=["Mesa"])
async def alterar_quantidade_integrantes(mesa_id: int, info: MesaInfo):
    return GP.alterar_numero_integrantes(mesa_id, info.numero_integrantes)


@app.put("/mesas/{mesa_id}/alterar-estado", tags=["Mesa"])
async def alterar_estado_do_pagamento(mesa_id: int, info: MesaInfo):
    return GP.atualizar_estado_pagamento(mesa_id, info.pago)


@app.get("/mesas/{mesa_id}", tags=["Mesa"])
async def buscar_mesa_por_id(mesa_id: int):
    return GP.buscar_mesa(mesa_id)


# Prato
@app.get("/pratos", tags=["Prato"])
async def listar_todos_os_pratos():
    return GP.listar_pratos()


@app.get("/pratos/categoria/{nome}", tags=["Prato"])
async def buscar_prato_por_categoria(nome: str):
    return GP.buscar_prato_por_categoria(nome)


@app.get("/pratos/tipo/{nome}", tags=["Prato"])
async def buscar_prato_por_tipo(nome: str):
    return GP.buscar_prato_por_tipo(nome)


@app.get("/pratos/id/{prato_id}", tags=["Prato"])
async def buscar_prato_por_id(prato_id: int):
    return GP.buscar_prato_por_id(prato_id)


@app.get("/pratos/nome/{nome}", tags=["Prato"])
async def buscar_prato_por_nome(nome: str):
    return GP.buscar_prato_por_nome(nome)


@app.post("/pratos/criar", tags=["Prato"])
async def criar_prato(info: PratoInfo):
    return GP.criar_prato(info.nome, info.preco, info.categoria, info.tipo)


@app.put("/pratos/alterar/{prato_id}", tags=["Prato"])
async def alterar_informacoes_do_prato(prato_id: int, info: PratoInfo):
    return GP.alterar_informacao_prato(prato_id, info.nome, info.preco, info.categoria, info.tipo)


@app.delete("/pratos/deletar/{prato_id}", tags=["Prato"])
async def deletar_prato(prato_id: int):
    return GP.deletar_prato_por_id(prato_id)


@app.post("/pedidos/criar", tags=["Pedido"])
async def criar_pedido(info: PedidoInfo):
    mesa = GP.buscar_mesa(info.id_mesa)
    prato = GP.buscar_prato_por_id(info.id_prato)
    print(mesa)
    print(prato)
    if mesa is None or prato is None:
        return None

    return GP.criar_pedido(prato, mesa, info.quantidade)


@app.get("/pedidos", tags=["Pedido"])
async def listar_pedidos():
    return GP.listar_pedidos()


@app.get("/pedidos/id/{pedido_id}", tags=["Pedido"])
async def buscar_pedido_por_id(pedido_id: int):
    return GP.buscar_pedido(pedido_id)


@app.get("/pedidos/mesa/{mesa_id}", tags=["Pedido"])
async def listar_pedidos_por_mesa(mesa_id: int):
    return GP.listar_pedidos_por_mesa(mesa_id)


@app.get("/pedidos/prato/{prato_id}", tags=["Pedido"])
async def listar_pedidos_por_prato(prato_id: int):
    return GP.listar_pedidos_por_prato(prato_id)


@app.get("/pedidos/entregue/{estado}", tags=["Pedido"])
async def listar_pedidos_por_estado(estado: bool):
    return GP.listar_pedidos_por_estado(estado)


@app.put("/pedidos/alterar-estado/{pedido_id}", tags=["Pedido"])
async def alterar_estado_do_pedido(pedido_id: int, info: PedidoAlterado):
    return GP.alterar_estado_do_pedido(pedido_id, info.entregue)


@app.put("/pedidos/alterar-prato/{pedido_id}", tags=["Pedido"])
async def alterar_prato_do_pedido(pedido_id: int, info: PedidoAlterado):
    return GP.alterar_prato_do_pedido(pedido_id, info.id_prato)


@app.put("/pedidos/alterar-quantidade/{pedido_id}", tags=["Pedido"])
async def alterar_quantidade_do_pedido(pedido_id: int, info: PedidoAlterado):
    return GP.alterar_quantidade_do_pedido(pedido_id, info.quantidade)


@app.delete("/pedidos/deletar/{pedido_id}", tags=["Pedido"])
async def alterar_prato_do_pedido(pedido_id: int):
    return GP.deletar_pedido(pedido_id)
