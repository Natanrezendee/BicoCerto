#!/bin/bash
# Uso: ./deploy.sh https://github.com/SEU_USUARIO/bb-emprestimos
# Antes: oc login (copie o comando em "Copy login command" no console do Sandbox)
REPO=$1

# 1) Banco de dados (template pronto do catalogo)
oc new-app postgresql-ephemeral \
  -p DATABASE_SERVICE_NAME=postgresql \
  -p POSTGRESQL_USER=bb -p POSTGRESQL_PASSWORD=bb123 -p POSTGRESQL_DATABASE=emprestimos

# 2) Microsservicos (OpenShift faz o build do Dockerfile de cada pasta)
oc new-app $REPO --context-dir=analise   --name=analise   --strategy=docker
oc new-app $REPO --context-dir=simulacao --name=simulacao --strategy=docker
oc new-app $REPO --context-dir=proposta  --name=proposta  --strategy=docker \
  -e DB_HOST=postgresql -e DB_NAME=emprestimos -e DB_USER=bb -e DB_PASSWORD=bb123
oc new-app $REPO --context-dir=gateway   --name=gateway   --strategy=docker

# 3) Route: expoe so o gateway, com HTTPS
oc expose service/gateway
oc patch route gateway -p '{"spec":{"tls":{"termination":"edge"}}}'

echo "URL publica:"; oc get route gateway -o jsonpath='https://{.spec.host}{"\n"}'
