from dataclasses import dataclass


@dataclass
class Prato:
    id_prato: int
    prato_nome: str
    preco: float
    prato_categoria: str
    prato_tipo: str

    def get_id(self) -> int:
        return self.id_prato

    def get_preco(self) -> float:
        return self.preco

    def get_nome(self) -> str:
        return self.prato_nome

    def get_categoria(self) -> str:
        return self.prato_categoria

    def get_tipo(self) -> str:
        return self.prato_tipo

    def __eq__(self, other):
        if type(other) != Prato:
            return False
        return True if self.id_prato == other.id_prato else False

    def __init__(self, id_prato: int, prato_nome: str, preco: float, prato_categoria: str, prato_tipo: str):
        self.id_prato = id_prato
        self.prato_nome = prato_nome
        self.preco = preco
        self.prato_categoria = prato_categoria
        self.prato_tipo = prato_tipo
