import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)
ROTAS = {
    "simulacao": os.getenv("SIMULACAO_URL", "http://simulacao:8080"),
    "propostas": os.getenv("PROPOSTA_URL", "http://proposta:8080"),
}


@app.get("/")
def home():
    return {"servico": "gateway BB emprestimos", "rotas": ["/simulacao", "/propostas"]}


@app.route("/<nome>", methods=["GET", "POST"])
def encaminhar(nome):
    if nome not in ROTAS:
        return {"erro": "rota nao encontrada"}, 404
    r = requests.request(
        request.method, f"{ROTAS[nome]}/{nome}",
        params=request.args, json=request.get_json(silent=True), timeout=15,
    )
    return Response(r.content, r.status_code, content_type=r.headers.get("Content-Type"))
