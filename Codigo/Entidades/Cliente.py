from dataclasses import dataclass


@dataclass(init=True, eq=True)
class Cliente:
    id: int
    nome: str
    cpf: str
    mesa: int
    forma_de_pagamento: str
    valor_total: float
