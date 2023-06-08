from Codigo.Entidades.Cliente import Cliente
from Codigo.Controladores import ControladorDeCliente
from Codigo.main import pool
def teste_campos(cpf: str, nome: str, mesa: int, forma_de_pagamento: str, total: float):
    cliente = Cliente(1, nome, cpf, mesa, forma_de_pagamento, total)

    assert cliente.id == 1, "O id tem que ser 1"
    assert cliente.nome == nome, "nome tem que ser {}".format(nome)
    assert cliente.mesa == mesa, "mesa tem que ser {}".format(mesa)
    assert cliente.forma_de_pagamento == forma_de_pagamento, "Forma de pagamaneto Tem que ser {}".format(forma_de_pagamento)
    assert cliente.valor_total == total, "O total tem que ser {}".format(total)


def testar_crud(nome: str, cpf: str, mesa: int, forma_de_pagamento: str, total: float):
    print("Iniciando teste do CRUD.")
    cliente = Cliente(1, nome, cpf, mesa, forma_de_pagamento, total)
    with pool.connection() as conn:
        cliente2 = ControladorDeCliente.criar_cliente(nome, cpf, mesa, forma_de_pagamento, total, conn)
        assert cliente.nome == cliente2.nome, "criar cliente falhou"
        print("\tCREATE funciona")

        cliente3 = ControladorDeCliente.buscar_por_nome(nome, conn)
        assert cliente.nome == cliente3.nome, "buscar por nome falhou"
        print("\tREAD funciona")

        cliente4 = ControladorDeCliente.deletar_por_id(cliente3.id, conn)
        assert cliente3 == cliente4
        print("\tDELETE funciona")


if __name__ == "__main__":
    teste_campos("gabriel", "XXX.XXX.XXX-XX", 1, "cartao", 10)
    print("teste dos campos concluidos.")

    testar_crud("gabriel", "XXX.XXX.XXX-XX", 1, "cartao", 10)
    print("teste do crud concluido.")
