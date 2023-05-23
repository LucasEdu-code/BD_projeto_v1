import GerenciadorDePedidos as GP

"""
# CRIA MESAS
GP.criar_mesa(3)
GP.criar_mesa(1)
GP.criar_mesa(4)
GP.criar_mesa(10)


# CRIAR PRATOS
GP.criar_prato("Macarrão", 25, "almoço", "comida")
GP.criar_prato("Lasanha", 30, "almoço", "comida")
GP.criar_prato("Sorvete", 15, "Sobremesa", "comida")
GP.criar_prato("Coca-Cola", 5, "Refrigerante", "bebida")
GP.criar_prato("Suco de laranja", 10, "Suco natural", "bebida")


# CRIAR PEDIDOS
# MESA 1 PEDE MACARRÃO E COCA-COLA
GP.criar_pedido(GP.buscar_prato_por_nome("Macarrão")[0], GP.buscar_mesa(1), 1)
GP.criar_pedido(GP.buscar_prato_por_nome("Coca-Cola")[0], GP.buscar_mesa(1), 2)

# MESA 2 PEDE LASANHA E SUCO
GP.criar_pedido(GP.buscar_prato_por_nome("Macarrão")[0], GP.buscar_mesa(2), 1)
GP.criar_pedido(GP.buscar_prato_por_nome("Suco de laranja")[0], GP.buscar_mesa(2), 1)

# MESA 3 PEDE SORVETE
GP.criar_pedido(GP.buscar_prato_por_nome("Sorvete")[0], GP.buscar_mesa(3), 3)

"""

# PEDIDO 1 E 2 FOREM ENTREGUE
GP.alterar_estado_do_pedido(1, True)
GP.alterar_estado_do_pedido(2, True)

# PEDIDO 4 FOI ENTREGUE, MAS NÃO O 3
GP.alterar_estado_do_pedido(3, False)
GP.alterar_estado_do_pedido(4, True)

# MESA 1 PAGOU E FECHOU
GP.atualizar_estado_pagamento(1, True)
GP.fechar_mesa(1)
