# Emprestimos Banco do Brasil - OpenShift (AP2)

Pastas: gateway, simulacao, proposta, analise (cada uma com app.py + Dockerfile).

## Passo a passo
1. Crie um repositorio no GitHub e suba TODAS essas pastas nele.
2. Crie conta no Developer Sandbox e abra o console.
3. Canto superior direito > "Copy login command" > rode o comando `oc login ...` no terminal
   (ou use o terminal web do Sandbox, icone ">_").
4. Rode: ./deploy.sh https://github.com/SEU_USUARIO/SEU_REPO
5. Espere os builds (acompanhe em Topology) e use a URL que o script imprime.

## Testes (troque URL pela sua)
curl URL/
curl "URL/simulacao?valor=10000&parcelas=12"
curl -X POST URL/propostas -H "Content-Type: application/json" -d '{"cliente":"Maria","valor":20000,"parcelas":24}'
curl -X POST URL/propostas -H "Content-Type: application/json" -d '{"cliente":"Joao","valor":80000,"parcelas":48}'
curl URL/propostas

## Opcional: autoscale (HPA) no servico de simulacao
oc set resources deployment/simulacao --requests=cpu=50m --limits=cpu=200m
oc autoscale deployment/simulacao --min=1 --max=3 --cpu-percent=70
