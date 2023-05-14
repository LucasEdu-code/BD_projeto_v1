import datetime
import unittest

from Entidades import Mesa, Cardapio, Pedido


class TestMesa(unittest.TestCase):
    def test_constructor(self):
        mesa = Mesa(0, 4, 0, False)
        self.assertEqual(mesa, Mesa(0, 4, 0, False))


class TestCardapio(unittest.TestCase):
    def test_Constructor(self):
        cardapio = Cardapio(0, "macarrão", "almoço/janta", "comida", 20)
        self.assertEqual(cardapio, Cardapio(0, "macarrão", "almoço/janta", "comida", 20))


class TestPedido(unittest.TestCase):
    def test_Constructor(self):
        pedido = Pedido(0, 0, 0, 1, False, datetime.datetime.now())
        self.assertEqual(pedido, Pedido(0, 0, 0, 1, False, datetime.datetime.now()))
