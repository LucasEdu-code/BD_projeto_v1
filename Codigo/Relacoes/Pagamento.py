from dataclasses import dataclass


@dataclass(init=True, eq=True)
class Pagamento:
    id: int
    metodo_pagamento: int
    mesa: int
    cliente: int

