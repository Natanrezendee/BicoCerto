from flask import Flask, request

app = Flask(__name__)
TAXA_MENSAL = 0.018  # 1,8% ao mes (valor ficticio)


@app.get("/")
def saude():
    return {"servico": "simulacao", "status": "ok"}


@app.get("/simulacao")
def simular():
    valor = float(request.args.get("valor", 10000))
    parcelas = int(request.args.get("parcelas", 12))
    i = TAXA_MENSAL
    parcela = valor * i / (1 - (1 + i) ** -parcelas)  # tabela Price
    return {
        "valor": valor,
        "parcelas": parcelas,
        "taxa_mensal": f"{i * 100:.1f}%",
        "valor_parcela": round(parcela, 2),
        "total_a_pagar": round(parcela * parcelas, 2),
    }
