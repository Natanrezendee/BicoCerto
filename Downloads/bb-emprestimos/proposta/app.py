import os
import requests
import psycopg2
from flask import Flask, request

app = Flask(__name__)
ANALISE_URL = os.getenv("ANALISE_URL", "http://analise:8080")


def conectar():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgresql"),
        dbname=os.getenv("DB_NAME", "emprestimos"),
        user=os.getenv("DB_USER", "bb"),
        password=os.getenv("DB_PASSWORD", "bb123"),
        connect_timeout=5,
    )
    with conn, conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS propostas (
                 id SERIAL PRIMARY KEY,
                 cliente TEXT, valor NUMERIC, parcelas INT, status TEXT)"""
        )
    return conn


@app.get("/")
def saude():
    return {"servico": "proposta", "status": "ok"}


@app.post("/propostas")
def criar():
    d = request.get_json(silent=True) or {}
    cliente = d.get("cliente", "Cliente Teste")
    valor = float(d.get("valor", 10000))
    parcelas = int(d.get("parcelas", 12))

    analise = requests.post(
        f"{ANALISE_URL}/analisar", json={"valor": valor}, timeout=10
    ).json()

    conn = conectar()
    with conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO propostas (cliente, valor, parcelas, status) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (cliente, valor, parcelas, analise["resultado"]),
        )
        novo_id = cur.fetchone()[0]
    conn.close()
    return {"id": novo_id, "cliente": cliente, "valor": valor,
            "parcelas": parcelas, "analise": analise}, 201


@app.get("/propostas")
def listar():
    conn = conectar()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT id, cliente, valor, parcelas, status FROM propostas ORDER BY id")
        linhas = cur.fetchall()
    conn.close()
    return {"propostas": [
        {"id": i, "cliente": c, "valor": float(v), "parcelas": p, "status": s}
        for i, c, v, p, s in linhas]}
