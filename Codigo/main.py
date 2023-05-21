import GerenciadorDePedidos as GP


prato = GP.buscar_prato_por_nome("coca-cola")[0]
mesa = GP.buscar_mesa(3)

print(GP.criar_pedido(prato, mesa, 1))
