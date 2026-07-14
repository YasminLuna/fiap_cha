# Oficina API — Fase 2 | Sprint 2

Esta etapa evolui a aplicação da Sprint 1 com os artefatos de infraestrutura e automação exigidos no Tech Challenge. O projeto mantém o back-end em FastAPI e PostgreSQL, organizado em Clean Architecture, e acrescenta containerização, Kubernetes, Terraform e CI/CD.

## O que foi incorporado

- Dockerfile multi-stage executando a aplicação com usuário não root.
- Docker Compose para aplicação e PostgreSQL em desenvolvimento local.
- Manifestos Kubernetes em `k8s/`.
- Deployment com probes, limites de recursos e contexto de segurança.
- Service, ConfigMap, Secret de exemplo, PostgreSQL com volume e NetworkPolicy.
- Horizontal Pod Autoscaler por CPU e memória.
- Terraform para criar um cluster Kind e o banco PostgreSQL.
- Pipeline GitHub Actions com lint, testes, cobertura, Bandit, Terraform, build, Trivy, deploy e smoke test.
- Script de carga para demonstrar o HPA.

## Estrutura relevante

```text
.github/workflows/ci-cd.yml
infra/
k8s/
scripts/
Dockerfile
docker-compose.yml
```

## Executar localmente

Crie o arquivo de configuração e suba o ambiente:

```bash
cp .env.example .env
docker compose up --build
```

A documentação Swagger estará em `http://localhost:8000/docs`.

### Problema de certificado SSL durante o build

O Dockerfile aceita os argumentos `PIP_INDEX_URL` e `PIP_TRUSTED_HOST`. Isso permite executar o build em redes que fazem inspeção HTTPS e apresentam certificado próprio.

O valor padrão já contempla o PyPI:

```bash
docker compose build --no-cache
docker compose up
```

Em ambiente corporativo, a solução preferencial é usar a autoridade certificadora da empresa. O argumento foi mantido para tornar o laboratório reproduzível sem bloquear a entrega.

## Testes

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

Resultado validado:

```text
5 testes aprovados
90,57% de cobertura
```

## Provisionar o cluster com Terraform

Pré-requisitos: Docker, Terraform e kubectl.

```bash
cd infra
terraform init
terraform plan
terraform apply
```

O Terraform cria:

- cluster Kubernetes local com Kind;
- namespace `oficina`;
- Secret do PostgreSQL;
- Deployment e Service do banco.

## Implantar a aplicação no Kubernetes

Na raiz do projeto:

```bash
./scripts/create-k8s-secret.sh
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/networkpolicy.yaml
```

Acompanhe o deploy:

```bash
kubectl get pods -n oficina
kubectl get hpa -n oficina
kubectl rollout status deployment/oficina-api -n oficina
```

Para acessar localmente:

```bash
kubectl port-forward -n oficina service/oficina-api 8000:80
```

## Demonstrar escalabilidade

Com o port-forward ativo:

```bash
./scripts/load-test.sh
kubectl get hpa -n oficina -w
kubectl get pods -n oficina -w
```

O HPA está configurado com mínimo de 2 e máximo de 8 réplicas, usando CPU e memória como métricas.

## Pipeline

O workflow `.github/workflows/ci-cd.yml` executa:

1. Ruff e testes com cobertura mínima de 80%.
2. Bandit para análise estática de segurança.
3. Formatação e validação do Terraform.
4. Build e publicação da imagem no GitHub Container Registry.
5. Scan da imagem com Trivy.
6. Criação de um cluster Kind no runner.
7. Deploy do PostgreSQL e dos manifestos Kubernetes.
8. Smoke test dos endpoints `/health` e `/ready`.

Imagem configurada:

```text
ghcr.io/yasminluna/fiap_cha:latest
```

## Identificação

- Participante: **Yasmin Luna**
- Repositório: `https://github.com/YasminLuna/fiap_cha`
