from dataclasses import dataclass
from datetime import date


# Objetivo de simular uma ORM


@dataclass
class Mesa:
    # Em python não há o conceito de variáveis privadas, públicas ou protegidas, mas há a convenção
    # de que uma variável com prefixo __ ou _ vai ser tratada como uma variável privada.
    #
    # A diferença entre __ e _, é que as que possuem __ vão ter seus nomes alterados pelo interpretador.

    __id: int
    __numero_integrantes: int
    __consumo_total: float
    __pag: bool

    # Construtor
    def __init__(self, mesa_id: int, numero_integrantes: int, consumo_total: float, pago: bool):
        self.__id = mesa_id
        self.__numero_integrantes = numero_integrantes
        self.__consumo_total = consumo_total
        self.__pago = pago


@dataclass
class Cardapio:
    __prato_id: int
    __prato_nome: str
    __prato_categoria: str
    __prato_tipo: str
    __prato_preco: float

    # Construtor
    def __int__(self, prato_id: int, prato_nome: str, prato_categoria: str, prato_tipo: str):
        self.__prato_id = prato_id
        self.__prato_nome = prato_nome
        self.__prato_categoria = prato_categoria
        self.prato_tipo = prato_tipo


@dataclass
class Pedido:
    __id: int
    __mesa_id: int
    __prato_id: int
    __quantidade: int
    __entregue: bool
    __data: date

    #Construtor
    def __int__(self, pedido_id: int, mesa_id: int, prato_id: int, quantidade: int, entregue: bool, data: date):
        self.__id = pedido_id
        self.__mesa_id = mesa_id
        self.__prato_id = prato_id
        self.__quantidade = quantidade
        self.__entregue = entregue
        self.__data = data
