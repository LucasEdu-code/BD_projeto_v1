from dataclasses import dataclass


@dataclass()
class Mesa:
    # Em python não há o conceito de variáveis privadas, públicas ou protegidas, mas há a convenção
    # de que uma variável com prefixo __ ou _ vai ser tratada como uma variável privada.
    #
    # A diferença entre __ e _, é que as que possuem __ vão ter seus nomes alterados pelo interpretador.

    id: int
    numero_integrantes: int
    consumo_total: float
    pago: bool

    # Métodos de Leitura
    def get_id(self) -> int:
        return self.id

    def get_integrantes(self) -> int:
        return self.numero_integrantes

    def get_consumo_total(self) -> float:
        return self.consumo_total

    def esta_pago(self):
        return self.pago

    # Métodos de Atualização
    # O id será uma propriedade inalterável
    def alterar_quantidade_integrantes(self, novo_valor: int):
        self.numero_integrantes = novo_valor

    def alterar_consumo_total(self, novo_valor: float):
        self.consumo_total = novo_valor

    def somar_ao_consumo(self, valor: float):
        self.consumo_total += valor

    def subtrair_do_consumo(self, valor: float):
        self.consumo_total = valor

    def alterar_pago(self, estado: bool):
        self.pago = estado

    # Construtor
    def __init__(self, id: int, numero_integrantes: int, consumo_total: float, pago: bool):
        self.id = id
        self.numero_integrantes = numero_integrantes
        self.consumo_total = consumo_total
        self.pago = pago

    def __eq__(self, other):
        if type(other) != Mesa:
            return False

        return True if self.id == other.__id_pedido else False
