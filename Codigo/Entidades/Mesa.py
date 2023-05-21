from dataclasses import dataclass


@dataclass()
class Mesa:
    # Em python não há o conceito de variáveis privadas, públicas ou protegidas, mas há a convenção
    # de que uma variável com prefixo __ ou _ vai ser tratada como uma variável privada.
    #
    # A diferença entre __ e _, é que as que possuem __ vão ter seus nomes alterados pelo interpretador.

    __id: int
    __numero_integrantes: int
    __consumo_total: float
    __pago: bool

    # Métodos de Leitura
    def mesa_id(self) -> int:
        return self.__id

    def integrantes(self) -> int:
        return self.__numero_integrantes

    def consumo_total(self) -> float:
        return self.__consumo_total

    def esta_pago(self):
        return self.__pago

    # Métodos de Atualização
    # O id será uma propriedade inalterável
    def alterar_quantidade_integrantes(self, novo_valor: int):
        self.__numero_integrantes = novo_valor

    def alterar_consumo_total(self, novo_valor: float):
        self.__consumo_total = novo_valor

    def somar_ao_consumo(self, valor: float):
        self.__consumo_total += valor

    def subtrair_do_consumo(self, valor: float):
        self.__consumo_total = valor

    def alterar_pago(self, estado: bool):
        self.__pago = estado

    # Construtor
    def __init__(self, id_mesa: int, numero_integrantes: int, consumo_total: float, pago: bool):
        self.__id = id_mesa
        self.__numero_integrantes = numero_integrantes
        self.__consumo_total = consumo_total
        self.__pago = pago

    def __eq__(self, other):
        if type(other) != Mesa:
            return False

        return True if self.__id == other.__id_pedido else False
