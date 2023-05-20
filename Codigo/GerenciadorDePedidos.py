from Entidades.Prato import Prato
import psycopg


def criar_prato(nome: str, preco: float, categoria: str, tipo: str):
    return Prato(0, nome, preco, categoria, tipo)


def enviar_prato(prato: Prato):
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute(""
                        "INSERT INTO prato ( preco, prato_nome, prato_categoria, prato_tipo)"
                        "VALUES (%s, %s, %s, %s)"
                        , (prato.get_preco(), prato.get_nome(), prato.get_categoria(), prato.get_tipo()))


def listar_pratos():
    lista = []
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato")
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_nome(nome: str):
    lista = []
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE prato_nome = '{}'".format(nome))
            for prato in cur.fetchall():
                lista.append(Prato(prato[0], prato[2], prato[1], prato[3], prato[4]))
            return lista


def buscar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM prato WHERE id_prato = {}".format(_id))
            prato = cur.fetchone()
            return Prato(prato[0], prato[2], prato[1], prato[3], prato[4])


def deletar_prato_por_id(_id: int) -> Prato:
    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM prato WHERE id_prato = {} RETURNING *".format(_id))
            delete_value = cur.fetchone()
            return Prato(delete_value[0], delete_value[2], delete_value[1], delete_value[3], delete_value[4])


def alterar_valores_prato(prato_alvo_id: int = 0, nome: str = "", preco: float = 0, categoria: str = "", tipo: str = ""):
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

    with psycopg.connect("dbname=postgres user=postgres password=123456789") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE prato SET preco = %s, prato_nome = %s, prato_categoria = %s, prato_tipo = %s "
                        "WHERE id_prato = %s"
                        , (preco, nome, categoria, tipo, prato_alvo_id))
