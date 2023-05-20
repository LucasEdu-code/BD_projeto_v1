from dataclasses import dataclass


@dataclass
class Prato:
    __prato_id: int
    __prato_nome: str
    __prato_preco: float
    __prato_categoria: str
    __prato_tipo: str

    def get_id(self) -> id:
        return self.__prato_id

    def get_preco(self) -> float:
        return self.__prato_preco

    def get_nome(self) -> str:
        return self.__prato_nome

    def get_categoria(self) -> str:
        return self.__prato_categoria

    def get_tipo(self) -> str:
        return self.__prato_tipo

    # Construtor
    def __int__(self, prato_id: int, prato_nome: str, preco:float, prato_categoria: str, prato_tipo: str):
        self.__prato_id = prato_id
        self.__prato_nome = prato_nome
        self.__prato_categoria = prato_categoria
        self.prato_tipo = prato_tipo

    def __eq__(self, other):
        if type(other) != Prato:
            return False
        return True if self.__prato_id == other.__prato_id else False
