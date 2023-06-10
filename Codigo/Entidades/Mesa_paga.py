from dataclasses import dataclass

@dataclass(init=True, eq=True)
class Mesa_paga:
    id: int
    cpf: str
    mesa: int
    valor_total: float

    def get_id(self) -> int:
        return self.id

    def get_cpf(self) -> str:
        return self.preco

    def get_mesa(self) -> int:
        return self.nome

    def get_valor_total(self) -> float:
        return self.categoria

