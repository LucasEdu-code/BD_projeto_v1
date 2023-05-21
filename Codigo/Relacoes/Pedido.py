from dataclasses import dataclass
from datetime import date


@dataclass
class Pedido:
    id_pedido: int
    id_mesa: int
    id_prato: int
    quantidade: int
    entregue: bool
    data: date

    def get_id(self):
        return self.id_pedido

    def get_mesa_id(self):
        return self.id_mesa

    def get_prato_id(self):
        return self.id_prato

    def get_quantidade(self):
        return self.quantidade

    def foi_entregue(self):
        return self.entregue

    def get_datetime(self):
        return self.data

    def alterar_mesa(self, nova_mesa: int):
        self.id_mesa = nova_mesa

    def alterar_prato(self, novo_prato: int):
        self.id_prato = novo_prato

    def alterar_quantidade(self, nova_quantidade: int):
        self.quantidade = nova_quantidade

    def alterar_estado(self, entregue: bool):
        self.entregue = entregue

    def __eq__(self, other):
        if type(other) != Pedido:
            return False
        return True if self.id_pedido == other.id_pedido else False

    def __int__(self, id_pedido: int, id_mesa: int, id_prato: int, quantidade: int, entregue: bool, data: date):
        self.id_pedido = id_pedido
        self.id_mesa = id_mesa
        self.id_prato = id_prato
        self.quantidade = quantidade
        self.entregue = entregue
        self.data = data
