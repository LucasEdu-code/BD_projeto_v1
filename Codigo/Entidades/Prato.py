from dataclasses import dataclass


@dataclass(init=True, eq=True)
class Prato:
    id: int
    nome: str
    preco: float
    categoria: int
    tipo: int
    quantidade_disponivel: int

    def get_id(self) -> int:
        return self.id

    def get_preco(self) -> float:
        return self.preco

    def get_nome(self) -> str:
        return self.nome

    def get_categoria(self) -> int:
        return self.categoria

    def get_tipo(self) -> int:
        return self.tipo

    def get_quantidade_disponivel(self) -> int:
        return self.quantidade_disponivel
