import psycopg

from psycopg.rows import class_row
from Codigo.Entidades.Mesa import Mesa
from Codigo.Entidades.Prato import Prato
from Codigo.Relacoes.Pedido import Pedido

DB_CONFIG = "dbname=projeto user=postgres password=622644le"

def listar_mesa_historico():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("SELECT * from historico.mesa")
            return cur.fetchall()
        
def buscar_mesa_historico_id(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("SELECT * from historico.mesa WHERE id_mesa = %s", (_id,))
            return cur.fetchone()
        
def buscar_mesa_id_historico(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Mesa)) as cur:
            cur.execute("SELECT * from historico.mesa WHERE id_mesa = %s", (_id,))
            return cur.fetchone()
        

def listar_prato_historico():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * from historico.prato")
            return cur.fetchall()

def buscar_prato_nome_historico(nome: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM historico.prato WHERE prato_nome = %s", (nome,))
            return cur.fetchall()


def buscar_prato_id_historico(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM historico.prato WHERE id_prato = %s", (_id,))
            return cur.fetchone()


def buscar_prato_categoria_historico(categoria: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM historico.prato WHERE prato_categoria = %s", (categoria,))
            return cur.fetchall()


def buscar_prato_tipo_historico(tipo: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM historico.prato WHERE prato_tipo = %s", (tipo,))
            return cur.fetchall()
    

        
def listar_pedido_historico():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from historico.pedido")
            return cur.fetchall()
        
def buscar_pedido_id_historico(_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from historico.pedido WHERE id_pedido = %s", (_id,))
            return cur.fetchone()


def buscar_pedidos_mesa_historico(mesa_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from historico.pedido WHERE id_mesa = %s", (mesa_id,))
            cur.fetchall()


def buscar_pedidos_prato_historico(prado_id: int):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Pedido)) as cur:
            cur.execute("SELECT * from historico.pedido WHERE id_prato = %s", (prado_id,))
            return cur.fetchall()
