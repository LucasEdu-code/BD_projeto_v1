from fastapi import HTTPException
from psycopg.rows import class_row
from psycopg import connection
from Codigo.Entidades.Mesa_paga import Mesa_paga


def listar_Mesas_pagas(conn: connection):
    with conn.cursor(row_factory=class_row(Mesa_paga)) as cur:
        cur.execute("SELECT * FROM mesa_paga ORDER BY id")
        return cur.fetchall()
    
def criar_Mesa_paga(id: int, cpf: str, mesa: int, valor_total: int, conn: connection):
    with conn.cursor(row_factory=class_row(Mesa_paga)) as cur:
        cur.execute("INSERT INTO mesa_paga (id, cpf, mesa, valor_total)"
                    "VALUES (%s, %s, %s, %s) RETURNING *",
                    (id, cpf, mesa, valor_total))
        return cur.fetchone()
    
def buscar_por_mesa(mesa: int, conn: connection):
    with conn.cursor(row_factory=class_row(Mesa_paga)) as cur:
        cur.execute("SELECT * FROM mesa_paga WHERE mesa = %s", (mesa,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
    
def buscar_por_cpf(cpf: str, conn: connection):
    with conn.cursor(row_factory=class_row(Mesa_paga)) as cur:
        cur.execute("SELECT * FROM mesa_paga WHERE cpf = %s", (cpf,))
        temp = cur.fetchone()
        if temp is None:
            raise HTTPException(status_code=404)
        return temp
    
