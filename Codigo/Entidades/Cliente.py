from dataclasses import dataclass


@dataclass(init=True, eq=True)
class Cliente:
    id: int
    nome: str
    cpf: str
