from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def saude():
    return {"servico": "analise", "status": "ok"}


@app.post("/analisar")
def analisar():
    dados = request.get_json(silent=True) or {}
    valor = float(dados.get("valor", 0))
    # Regra ficticia: ate R$ 50.000 aprova, acima reprova
    if valor <= 50000:
        return {"resultado": "APROVADA", "motivo": "Dentro do limite de credito"}
    return {"resultado": "REPROVADA", "motivo": "Acima do limite de credito"}
