from dataclasses import dataclass


@dataclass(init=True, eq=True)
class MetodoPagamento:
    id: int
    nome: str
