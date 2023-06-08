import psycopg_pool

DB_CONFIG = "dbname=postgres user=postgres password=123456789"

pool = psycopg_pool.ConnectionPool(conninfo=DB_CONFIG)