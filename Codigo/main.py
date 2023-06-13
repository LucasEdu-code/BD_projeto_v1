from datetime import datetime

import psycopg_pool

from Codigo.Controladores import ControladorDoHistorico, ControladorDeMesa, ControladorDePedido, ControladorDePrato, \
    ControladorDeTipo, ControladorDeCategoria, ControladorDeMesa_paga, ControladorDeCliente, \
    ControladorDeMetodoPagamento, ControladorDePagamento

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
    quantidade_disponivel: int | None = None


class PedidoInfo(BaseModel):
    id_mesa: int | None = None
    id_prato: int | None = None
    quantidade: int | None = None
    entregue: bool | None = None


class tipoInfo(BaseModel):
    id: int | None = None
    nome: str | None = None


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


@app.put("/mesas/fechar/{mesa_id}", tags=["Mesa"])
async def fechar_mesa(mesa_id: int):
    with pool.connection() as conn:
        mesa = ControladorDeMesa.buscar_mesa(mesa_id, conn)
        if mesa.esta_pago():
            ControladorDePedido.salvar_pedidos(mesa, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Prato
@app.get("/pratos", tags=["Prato"])
async def listar_todos_os_pratos():
    with pool.connection() as conn:
        temp = ControladorDePrato.listar_pratos(conn)
        return temp


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
        return ControladorDePrato.criar_prato(info.nome, info.preco, info.categoria, info.tipo,
                                              info.quantidade_disponivel, conn)


@app.put("/pratos/alterar/{prato_id}", tags=["Prato"])
async def alterar_informacoes_do_prato(prato_id: int, info: PratoInfo):
    with pool.connection() as conn:
        return ControladorDePrato.alterar_informacao_prato(conn, prato_id, info.nome, info.preco, info.categoria,
                                                           info.tipo)


@app.delete("/pratos/deletar/{prato_id}", tags=["Prato"])
async def deletar_prato(prato_id: int):
    with pool.connection() as conn:
        return ControladorDePrato.deletar_prato_por_id(prato_id, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# pedido


@app.get("/pedidos/buscar/tempo/{inicio}/{fim}")
async def buscar_periodo(inicio: str, fim: str):
    with pool.connection() as conn:
        return ControladorDePedido.buscar_por_periodo(inicio, fim, conn)


@app.get("/pedidos/quantidade", tags=["Pedido"])
async def quantidade_de_pedidos():
    with pool.connection() as conn:
        return ControladorDePedido.quantidade(conn)


@app.get("/pedidos/custo_total", tags=["Pedido"])
async def custo_total_de_pedidos():
    with pool.connection() as conn:
        return ControladorDePedido.custo_total(conn)


@app.get("/pedidos/listar", tags=["Pedido"])
async def listar_com_view():
    with pool.connection() as conn:
        return ControladorDePedido.listar_pedidos_com_view(conn)


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


@app.get("/pedidos/buscar/categoria/{categoria_id}", tags=["Pedido"])
async def listar_pedidos_por_prato(categoria_id: int):
    with pool.connection() as conn:
        return ControladorDePedido.listar_pedidos_por_categoria(categoria_id, conn)


@app.get("/pedidos/buscar/tipo/{tipo_id}", tags=["Pedido"])
async def listar_pedidos_por_prato(tipo_id: int):
    with pool.connection() as conn:
        return ControladorDePedido.listar_pedidos_por_tipo(tipo_id, conn)


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
        pedido = ControladorDePedido._buscar_pedido(pedido_id, conn)
        return ControladorDePedido.deletar_pedido(pedido, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Historico
@app.get("/historico/mesas", tags=["Historico"])
async def listar_historico_mesa():
    return ControladorDoHistorico.listar_mesa_historico()


@app.get("/historico/{historico_id}", tags=["Historico"])
async def buscar_historico_id_mesa(historico_id: int):
    return ControladorDoHistorico.buscar_mesa_historico_id(historico_id)


@app.get("/historico/mesas/{mesa_id}", tags=["Historico"])
async def buscar_historico_mesa_id(mesa_id: int):
    return ControladorDoHistorico.buscar_mesa_id_historico(mesa_id)


@app.get("/historico/pratos", tags=["Historico"])
async def listar_historico_prato():
    return ControladorDoHistorico.listar_prato_historico()


@app.get("/historico/pratos/id/{prato_id}", tags=["Historico"])
async def listar_historico_prato_id(prato_id: int):
    return ControladorDoHistorico.buscar_prato_id_historico(prato_id)


@app.get("/historico/pratos/nome/{nome}", tags=["Historico"])
async def buscar_prato_nome_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_nome_historico(nome)


@app.get("/historico/pratos/tipo/{nome}", tags=["Historico"])
async def buscar_prato_tipo_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_tipo_historico(nome)


@app.get("/historico/pratos/categoria/{nome}", tags=["Historico"])
async def buscar_prato_categoria_historico(nome: str):
    return ControladorDoHistorico.buscar_prato_categoria_historico(nome)


@app.get("/historico/pedidos", tags=["Historico"])
async def listar_pedidos_historico():
    return ControladorDoHistorico.listar_pedido_historico()


@app.get("/historico/pedidos/id/{pedido_id}", tags=["Historico"])
async def buscar_pedido_id_historico(pedido_id: int):
    return ControladorDoHistorico.buscar_pedido_id_historico(pedido_id)


@app.get("/historico/pedidos/mesa/{mesa_id}", tags=["Historico"])
async def buscar_pedidos_mesa_historico(mesa_id: int):
    return ControladorDoHistorico.buscar_pedidos_mesa_historico(mesa_id)


@app.get("/historico/pedidos/prato/{prato_id}", tags=["Historico"])
async def buscar_pedidos_prato_historico(prato_id: int):
    return ControladorDoHistorico.buscar_pedidos_prato_historico(prato_id)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Tipos
@app.get("/tipos", tags=["tipos"])
def listar_todos():
    with pool.connection() as conn:
        return ControladorDeTipo.listar_tipos(conn)


@app.get("/tipos/buscar/id/{id}", tags=["tipos"])
def buscar(id: int):
    with pool.connection() as conn:
        return ControladorDeTipo.buscar_id(id, conn)


@app.post("/tipos/criar", tags=["tipos"])
def criar_tipo(info: tipoInfo):
    with pool.connection() as conn:
        return ControladorDeTipo.criar_tipo(info.nome, conn)


@app.put("/tipos/alterar/{id}", tags=["tipos"])
def alterar_nome(info: tipoInfo, id: int):
    with pool.connection() as conn:
        tipo = ControladorDeTipo.buscar_id(id, conn)
        return ControladorDeTipo.alterar_nome(tipo.nome, info.nome, conn)


@app.delete("/tipos/deletar/{id}", tags=["tipos"])
def deletar_tipo(id: int):
    with pool.connection() as conn:
        return ControladorDeTipo.deletar_tipo(id, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Categorias
@app.get("/categorias", tags=["tipos"])
def listar_todos():
    with pool.connection() as conn:
        return ControladorDeCategoria.listar_categorias(conn)


@app.get("/categorias/buscar/id/{id}", tags=["tipos"])
def listar_todos(id: int):
    with pool.connection() as conn:
        return ControladorDeCategoria.buscar_id(id, conn)


@app.post("/categorias/criar", tags=["tipos"])
def criar_tipo(info: tipoInfo):
    with pool.connection() as conn:
        return ControladorDeCategoria.criar_categoria(info.nome, conn)


@app.delete("/categorias/deletar/{id}", tags=["tipos"])
def deletar_tipo(id: int):
    with pool.connection() as conn:
        return ControladorDeCategoria.deletar_categoria(id, conn)


@app.put("/categorias/alterar/{id}", tags=["tipos"])
def alterar_nome(info: tipoInfo, id: int):
    with pool.connection() as conn:
        tipo = ControladorDeCategoria.buscar_id(id, conn)
        return ControladorDeCategoria.alterar_nome(tipo.nome, info.nome, conn)


# ////////////////////////////////////////////////////////////////////////////////////////////////
# Cliente

class ClienteInfo(BaseModel):
    nome: str | None = None
    cpf: str | None = None


# CREATE
@app.post("/cliente/criar", tags=["Cliente"])
async def criar_cliente(info: ClienteInfo):
    with pool.connection() as conn:
        return ControladorDeCliente.criar(info.nome, info.cpf, conn)


# READ
@app.get("/cliente", tags=["Cliente"])
async def listar_clientes():
    with pool.connection() as conn:
        return ControladorDeCliente.listar_clientes(conn)


@app.get("/cliente/buscar/nome/{nome}", tags=["Cliente"])
async def buscar_cliente_por_nome(nome: str):
    with pool.connection() as conn:
        return ControladorDeCliente.buscar_por_nome(nome, conn)


@app.get("/cliente/buscar/id/{id}", tags=["Cliente"])
async def buscar_cliente_por_nome(id: int):
    with pool.connection() as conn:
        return ControladorDeCliente.buscar(id, conn)


@app.put("/cliente/modificar/{cliente_id}", tags=["Cliente"])
async def modificar(cliente_id: int, info: ClienteInfo):
    with pool.connection() as conn:
        return ControladorDeCliente.modificar(cliente_id, info.nome, info.cpf, conn)


@app.delete("/cliente/deletar/{id}", tags=["Cliente"])
def deletar_cliente_id(id: int):
    with pool.connection() as conn:
        return ControladorDeCliente.deletar_por_id(id, conn)


@app.delete("/cliente/deletar/{nome}", tags=["Cliente"])
def deletar_cliente_nome(nome: str):
    with pool.connection() as conn:
        return ControladorDeCliente.deletar_por_nome(nome, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////
# Mesa_paga

class pagamento_info(BaseModel):
    metodo_id: int
    cliente_id: int


@app.post("/pagamento/pagar/{mesa_id}", status_code=200)
async def pagar(mesa_id: int, info: pagamento_info):
    with pool.connection() as conn:
        mesa = ControladorDeMesa.buscar_mesa(mesa_id, conn)

        ControladorDePagamento.efetuar_pagamento(info.cliente_id, mesa.get_id(), info.metodo_id, conn)


@app.get("/pagamento/{cliente_id}")
async def listar(cliente_id: int):
    with pool.connection() as conn:
        return ControladorDePagamento.listar(cliente_id, conn)


@app.get("/Mesa_paga", tags=["Mesa_paga"])
async def listar_Mesas_pagas():
    with pool.connection() as conn:
        return ControladorDeMesa_paga.listar_Mesas_pagas(conn)


@app.get("/Mesa_paga/buscar/{mesa}", tags=["Mesa_paga"])
async def buscar_MesaPaga_por_mesa(mesa: int):
    with pool.connection() as conn:
        return ControladorDeMesa_paga.buscar_por_mesa(mesa, conn)


@app.get("/Cliente/buscar/{cpf}", tags=["Mesa_paga"])
async def buscar_MesaPaga_por_cpf(cpf: str):
    with pool.connection() as conn:
        return ControladorDeMesa_paga.buscar_por_cpf(cpf, conn)


# ///////////////////////////////////////////////////////////////////////////////////////////////
# Metodo de Pagamento
class pagamento_info(BaseModel):
    id: int | None = None
    nome: str | None = None


# CREATE
@app.post("/metodoPagamento")
async def criar_metodo_de_pagamento(info: pagamento_info):
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.criar(info.nome, conn)


# READ
@app.get("/metodoPagamento")
async def listar_metodos():
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.listar(conn)


@app.get("/metodoPagamento/{id}")
async def buscar_metodo(id: int):
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.buscar(id, conn)


@app.get("/metodoPagamento/{nome}")
async def buscar_por_nome(nome: str):
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.buscar_por_nome(nome, conn)


# UPDATE
@app.put("/metodoPagamento/{id}")
async def atualizar_nome(id: int, info: pagamento_info):
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.mudar_nome(id, info.nome, conn)


# DELETE
@app.delete("/metodoPagamento/{id}")
async def deletar(id: int):
    with pool.connection() as conn:
        return ControladorDeMetodoPagamento.deletar(id, conn)

# ///////////////////////////////////////////////////////////////////////////////////////////////
# Cliente

# CREATE
