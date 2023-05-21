import GerenciadorDePedidos as GP
from fastapi import FastAPI


app = FastAPI()


@app.get("/pratos")
async def listar_pratos():
    return GP.listar_pratos()


@app.get("/mesas")
async def listar_mesas():
    return GP.listar_mesas()


@app.get("/pedidos")
async def listar_pedidos():
    return GP.listar_pedidos()