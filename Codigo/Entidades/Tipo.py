from dataclasses import dataclass


@dataclass(init=True, eq=True)
class Tipo:
    id: int
    nome: str

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def set_nome(self, novo_nome):
        self.nome = novo_nome
