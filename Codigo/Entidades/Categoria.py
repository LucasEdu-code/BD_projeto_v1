from dataclasses import dataclass


@dataclass(init=True)
class Categoria:
    id: int
    nome: str

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def set_nome(self, novo_nome):
        self.nome = novo_nome

    def __eq__(self, other):
        if type(other) != Categoria:
            return False
        return True if self.id == other.id else False
