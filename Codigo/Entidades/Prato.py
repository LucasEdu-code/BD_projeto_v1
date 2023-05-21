from dataclasses import dataclass


@dataclass
class Prato:
    __id_prato: int
    __prato_nome: str
    __preco: float
    __prato_categoria: str
    __prato_tipo: str

    def get_id(self) -> int:
        return self.__id_prato

    def get_preco(self) -> float:
        return self.__preco

    def get_nome(self) -> str:
        return self.__prato_nome

    def get_categoria(self) -> str:
        return self.__prato_categoria

    def get_tipo(self) -> str:
        return self.__prato_tipo

    def __eq__(self, other):
        if type(other) != Prato:
            return False
        return True if self.__id_prato == other.__id_prato else False

    def __init__(self, id_prato: int, prato_nome: str, preco: float, prato_categoria: str, prato_tipo: str):
        self.__id_prato = id_prato
        self.__prato_nome = prato_nome
        self.__preco = preco
        self.__prato_categoria = prato_categoria
        self.__prato_tipo = prato_tipo
