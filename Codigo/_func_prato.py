import psycopg

from psycopg.rows import class_row
from Codigo.Entidades.Prato import Prato

DB_CONFIG = "dbname=projeto user=postgres password=622644le"

def criar_prato(nome: str, preco: float, categoria: str, tipo: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute(""
                        "INSERT INTO prato (prato_nome, preco, prato_categoria, prato_tipo)"
                        "VALUES (%s, %s, %s, %s) RETURNING *",
                        (nome, preco, categoria, tipo))
            return cur.fetchone()


def listar_pratos():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato")
            return cur.fetchall()


def buscar_prato_por_nome(nome: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_nome = %s", (nome,))
            return cur.fetchall()


def buscar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE id_prato = %s", (_id,))
            return cur.fetchone()


def buscar_prato_por_categoria(categoria: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_categoria = %s", (categoria,))
            return cur.fetchall()


def buscar_prato_por_tipo(tipo: str):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("SELECT * FROM prato WHERE prato_tipo = %s", (tipo,))
            return cur.fetchall()


def deletar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("DELETE FROM prato WHERE id_prato = %s RETURNING *", (_id,))
            return cur.fetchone()


def alterar_informacao_prato(prato_alvo_id: int = 0, nome: str = "", preco: float = 0, categoria: str = "",
                             tipo: str = ""):
    if prato_alvo_id == 0:
        return

    prato_alvo = buscar_prato_por_id(prato_alvo_id)

    if nome == "":
        nome = prato_alvo.get_nome()

    if preco == 0:
        preco = prato_alvo.get_preco()

    if categoria == "":
        categoria = prato_alvo.get_categoria()

    if tipo == "":
        tipo = prato_alvo.get_tipo()

    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=class_row(Prato)) as cur:
            cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                        "WHERE id_prato = %s RETURNING *",
                        (preco, nome, categoria, tipo, prato_alvo_id))
            return cur.fetchone()