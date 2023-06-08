from dataclasses import dataclass


@dataclass
class Prato:
    id: int
    prato_nome: str
    preco: float
    prato_categoria: int
    prato_tipo: int

    def get_id(self) -> int:
        return self.id

    def get_preco(self) -> float:
        return self.preco

    def get_nome(self) -> str:
        return self.prato_nome

    def get_categoria(self) -> int:
        return self.prato_categoria

    def get_tipo(self) -> int:
        return self.prato_tipo

    def __eq__(self, other):
        if type(other) != Prato:
            return False
        return True if self.id == other.id_prato else False

    def __init__(self, id: int, nome: str, preco: float, categoria: str, tipo: str):
        self.id = id
        self.prato_nome = nome
        self.preco = preco
        self.prato_categoria = categoria
        self.prato_tipo = tipo
