from dataclasses import dataclass
from datetime import date


@dataclass
class Pedido:
    __id: int
    __id_mesa: int
    __id_prato: int
    __quantidade: int
    __entregue: bool
    __data: date

    def get_id(self):
        return self.__id

    def get_mesa_id(self):
        return self.__id_mesa

    def get_prato_id(self):
        return self.__id_prato

    def get_quantidade(self):
        return self.__quantidade

    def foi_entregue(self):
        return self.__entregue

    def get_datetime(self):
        return self.__data

    def alterar_mesa(self, nova_mesa: int):
        self.__id_mesa = nova_mesa

    def alterar_prato(self, novo_prato: int):
        self.__id_prato = novo_prato

    def alterar_quantidade(self, nova_quantidade: int):
        self.__quantidade = nova_quantidade

    def alterar_estado(self, entregue: bool):
        self.__entregue = entregue

    def __int__(self, pedido_id: int, mesa_id: int, prato_id: int, quantidade: int, entregue: bool, data: date):
        self.__id = pedido_id
        self.__id_mesa = mesa_id
        self.__id_prato = prato_id
        self.__quantidade = quantidade
        self.__entregue = entregue
        self.__data = data

    def __eq__(self, other):
        if type(other) != Pedido:
            return False
        return True if self.__id == other.__id else False
