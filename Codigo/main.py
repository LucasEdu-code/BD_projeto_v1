import Codigo._func_historico as F_historico
import Codigo._func_mesa as F_mesa
import Codigo._func_pedido as F_pedido
import Codigo._func_prato as F_prato


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    return F_mesa.listar_mesas()


@app.post("/mesas/criar", tags=["Mesa"])
async def criar_mesa(info: MesaInfo):
    return F_mesa.criar_mesa(info.numero_integrantes)


@app.delete("/mesas/deletar/{mesa_id}", tags=["Mesa"])
async def deletar_mesa(mesa_id: int):
    return F_mesa.deletar_mesa(mesa_id)


@app.put("/mesas/{mesa_id}/alterar-qnt-integrantes", tags=["Mesa"])
async def alterar_quantidade_integrantes(mesa_id: int, info: MesaInfo):
    return F_mesa.alterar_numero_integrantes(mesa_id, info.numero_integrantes)


@app.put("/mesas/{mesa_id}/alterar-estado", tags=["Mesa"])
async def alterar_estado_do_pagamento(mesa_id: int, info: MesaInfo):
    return F_mesa.atualizar_estado_pagamento(mesa_id, info.pago)


@app.get("/mesas/{mesa_id}", tags=["Mesa"])
async def buscar_mesa_por_id(mesa_id: int):
    return F_mesa.buscar_mesa(mesa_id)


# Prato
@app.get("/pratos", tags=["Prato"])
async def listar_todos_os_pratos():
    return F_prato.listar_pratos()


@app.get("/pratos/categoria/{nome}", tags=["Prato"])
async def buscar_prato_por_categoria(nome: str):
    return F_prato.buscar_prato_por_categoria(nome)


@app.get("/pratos/tipo/{nome}", tags=["Prato"])
async def buscar_prato_por_tipo(nome: str):
    return F_prato.buscar_prato_por_tipo(nome)


@app.get("/pratos/id/{prato_id}", tags=["Prato"])
async def buscar_prato_por_id(prato_id: int):
    return F_prato.buscar_prato_por_id(prato_id)


@app.get("/pratos/nome/{nome}", tags=["Prato"])
async def buscar_prato_por_nome(nome: str):
    return F_prato.buscar_prato_por_nome(nome)


@app.post("/pratos/criar", tags=["Prato"])
async def criar_prato(info: PratoInfo):
    return F_prato.criar_prato(info.nome, info.preco, info.categoria, info.tipo)


@app.put("/pratos/alterar/{prato_id}", tags=["Prato"])
async def alterar_informacoes_do_prato(prato_id: int, info: PratoInfo):
    return F_prato.alterar_informacao_prato(prato_id, info.nome, info.preco, info.categoria, info.tipo)


@app.delete("/pratos/deletar/{prato_id}", tags=["Prato"])
async def deletar_prato(prato_id: int):
    return F_prato.deletar_prato_por_id(prato_id)

#pedido
@app.post("/pedidos/criar", tags=["Pedido"])
async def criar_pedido(info: PedidoInfo):
    mesa = F_mesa.buscar_mesa(info.id_mesa)
    prato = F_prato.buscar_prato_por_id(info.id_prato)
    print(mesa)
    print(prato)
    if mesa is None or prato is None:
        return None

    return F_pedido.criar_pedido(prato, mesa, info.quantidade)


@app.get("/pedidos", tags=["Pedido"])
async def listar_pedidos():
    return F_pedido.listar_pedidos()


@app.get("/pedidos/id/{pedido_id}", tags=["Pedido"])
async def buscar_pedido_por_id(pedido_id: int):
    return F_pedido.buscar_pedido(pedido_id)


@app.get("/pedidos/mesa/{mesa_id}", tags=["Pedido"])
async def listar_pedidos_por_mesa(mesa_id: int):
    return F_pedido.listar_pedidos_por_mesa(mesa_id)


@app.get("/pedidos/prato/{prato_id}", tags=["Pedido"])
async def listar_pedidos_por_prato(prato_id: int):
    return F_pedido.listar_pedidos_por_prato(prato_id)


@app.get("/pedidos/entregue/{estado}", tags=["Pedido"])
async def listar_pedidos_por_estado(estado: bool):
    return F_pedido.listar_pedidos_por_estado(estado)


@app.put("/pedidos/alterar-estado/{pedido_id}", tags=["Pedido"])
async def alterar_estado_do_pedido(pedido_id: int, info: PedidoAlterado):
    return F_pedido.alterar_estado_do_pedido(pedido_id, info.entregue)


@app.put("/pedidos/alterar-prato/{pedido_id}", tags=["Pedido"])
async def alterar_prato_do_pedido(pedido_id: int, info: PedidoAlterado):
    return F_pedido.alterar_prato_do_pedido(pedido_id, info.id_prato)


@app.put("/pedidos/alterar-quantidade/{pedido_id}", tags=["Pedido"])
async def alterar_quantidade_do_pedido(pedido_id: int, info: PedidoAlterado):
    return F_pedido.alterar_quantidade_do_pedido(pedido_id, info.quantidade)


@app.delete("/pedidos/deletar/{pedido_id}", tags=["Pedido"])
async def alterar_prato_do_pedido(pedido_id: int):
    return F_pedido.deletar_pedido(pedido_id)


@app.put("/mesas/fechar/{mesa_id}", tags=["Fechar"])
async def fechar_mesa(mesa_id: int):
    if F_mesa.buscar_mesa(mesa_id).pago:
        F_pedido.salvar_pedidos(mesa_id)

@app.get("/historico/mesas", tags=["Historico_mesa"])
async def listar_historico_mesa():
    return F_historico.listar_mesa_historico()

@app.get("/historico/{historico_id}", tags=["Historico_mesa"])
async def buscar_historico_id_mesa(historico_id: int):
    return F_historico.buscar_mesa_historico_id(historico_id)

@app.get("/historico/mesas/{mesa_id}", tags=["Historico_mesa"])
async def buscar_historico_mesa_id(mesa_id: int):
    return F_historico.buscar_mesa_id_historico(mesa_id)

@app.get("/historico/pratos", tags=["Historico_prato"])
async def listar_historico_prato():
    return F_historico.listar_prato_historico()

@app.get("/historico/pratos/id/{prato_id}", tags=["Historico_prato"])
async def listar_historico_prato_id(prato_id: int):
    return F_historico.buscar_prato_id_historico(prato_id)

@app.get("/historico/pratos/nome/{nome}", tags=["Historico_prato"])
async def buscar_prato_nome_historico(nome: str):
    return F_historico.buscar_prato_nome_historico(nome)

@app.get("/historico/pratos/tipo/{nome}", tags=["Historico_prato"])
async def buscar_prato_tipo_historico(nome: str):
    return F_historico.buscar_prato_tipo_historico(nome)

@app.get("/historico/pratos/categoria/{nome}", tags=["Historico_prato"])
async def buscar_prato_categoria_historico(nome: str):
    return F_historico.buscar_prato_categoria_historico(nome)

@app.get("/historico/pedidos", tags=["Historico_pedido"])
async def listar_pedidos_historico():
    return F_historico.listar_pedido_historico()

@app.get("/historico/pedidos/id/{pedido_id}", tags=["Historico_pedido"])
async def buscar_pedido_id_historico(pedido_id: int):
    return F_historico.buscar_pedido_id_historico(pedido_id)

@app.get("/historico/pedidos/mesa/{mesa_id}", tags=["Historico_pedido"])
async def buscar_pedidos_mesa_historico(mesa_id: int):
    return F_historico.buscar_pedidos_mesa_historico(mesa_id)

@app.get("/historico/pedidos/prato/{prato_id}", tags=["Historico_pedido"])
async def buscar_pedidos_prato_historico(prato_id: int):
    return F_historico.buscar_pedidos_prato_historico(prato_id)






