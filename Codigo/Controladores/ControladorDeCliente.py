from fastapi import HTTPException
from psycopg.rows import class_row, dict_row
from psycopg import connection
from Codigo.Entidades.Cliente import Cliente


def listar_clientes(conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("SELECT * FROM cliente ORDER BY id")
        return cur.fetchall()


def criar(nome: str, cpf: str, conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("INSERT INTO cliente (nome, cpf) "
                    "VALUES (%s, %s) RETURNING *",
                    (nome, cpf))
        return cur.fetchone()


def buscar_por_nome(nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("SELECT * FROM cliente WHERE nome = %s", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def buscar(id: int, conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("SELECT * FROM cliente WHERE id = %s", (id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def deletar_por_id(_id: int, conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("DELETE FROM cliente WHERE id = %s RETURNING *", (_id,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def deletar_por_nome(nome: str, conn: connection):
    with conn.cursor(row_factory=class_row(Cliente)) as cur:
        cur.execute("DELETE FROM cliente WHERE nome = %s RETURNING *", (nome,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp


def modificar(cliente_id: int, nome: str, cpf: str, conn: connection):
    with conn.cursor(row_factory=dict_row) as cur:
        if nome != "" and nome is not None:
            cur.execute("UPDATE cliente SET nome = %s WHERE id = %s",
                        (nome, cliente_id))

        if cpf != "" and cpf is not None:
            cur.execute("UPDATE cliente SET cpf = %s WHERE id = %s",
                        (cpf, cliente_id))

        cur.execute("SELECT * from cliente WHERE id = %s", (cliente_id,))
        return cur.fetchone()

