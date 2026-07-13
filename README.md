# Oficina API — Tech Challenge Fase 2

Evolução do MVP da Fase 1 para uma solução com **Clean Architecture, testes automatizados, Docker, Kubernetes, Terraform e CI/CD**. O sistema controla clientes, veículos, catálogo de serviços, peças e ordens de serviço, incluindo orçamento, aprovação externa e acompanhamento de status.

## Decisões principais

- **Python + FastAPI:** API legível, tipada e com Swagger automático.
- **PostgreSQL:** consistência transacional para estoque, orçamento e histórico.
- **Monólito modular:** adequado ao porte do MVP, sem custo operacional prematuro de microsserviços.
- **Clean Architecture:** regras de negócio isoladas de HTTP e persistência.
- **Kubernetes + HPA:** disponibilidade e escala horizontal por CPU/memória.
- **Terraform:** cluster local Kind e banco reproduzíveis.

A arquitetura e o fluxo de deploy estão em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Requisitos implementados

- Abertura de OS com cliente, veículo, serviços e peças, retornando ID único.
- Consulta pública do status e detalhes da OS.
- Webhook de aprovação ou recusa de orçamento.
- Listagem ativa priorizada: Execução, Aguardando Aprovação, Diagnóstico e Recebida; mais antigas primeiro.
- OS finalizadas, entregues ou canceladas ficam fora da listagem operacional.
- Atualização de status com notificação por SMTP; sem SMTP, o evento é registrado em log.
- CRUD de criação/listagem para clientes, veículos, serviços e peças.
- JWT, validações, testes, métricas, health e readiness.

## Execução local

```bash
cp .env.example .env
docker compose up --build
```

Acesse:

- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`
- Métricas: `http://localhost:8000/metrics`

Credenciais locais: `admin@oficina.example.com` / `Admin123!`.

## Testes e qualidade

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check app tests
pytest
bandit -r app -ll
```

A suíte exige cobertura mínima de 80% e cobre o fluxo crítico de abertura, evolução de status, aprovação e priorização das ordens.

## Terraform

Pré-requisitos: Terraform, Docker, kubectl e Kind compatíveis.

```bash
cd infra
terraform init
terraform plan
terraform apply
```

Recursos: cluster Kind com três nós, namespace `oficina`, Secret, PostgreSQL Deployment e Service. Consulte [`infra/README.md`](infra/README.md).

## Deploy Kubernetes

1. Crie o secret a partir do exemplo, sem versionar valores reais.
2. A imagem padrão já aponta para `ghcr.io/yasminluna/fiap_cha:latest`.
3. Aplique os manifestos:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -k k8s/
kubectl get pods,svc,hpa -n oficina
```

Para acesso local:

```bash
kubectl port-forward -n oficina service/oficina-api 8000:80
```

## Demonstração do HPA

O Metrics Server precisa estar ativo. Em outro terminal:

```bash
kubectl get hpa -n oficina -w
./scripts/load-test.sh http://localhost:8000/health
```

## CI/CD

O GitHub Actions executa lint, testes com cobertura, Bandit, build e publicação da imagem no GHCR, scan Trivy, deploy em cluster Kind e smoke test. O workflow está em `.github/workflows/ci-cd.yml`.

## Fluxo de status

`RECEIVED → DIAGNOSIS → AWAITING_APPROVAL → IN_PROGRESS → FINISHED → DELIVERED`

Uma recusa de orçamento move a OS de `AWAITING_APPROVAL` para `CANCELLED`.

## Materiais de entrega

- Arquitetura: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Roteiro do vídeo: [`docs/VIDEO_SCRIPT_PHASE2.md`](docs/VIDEO_SCRIPT_PHASE2.md)
- Segurança: [`SECURITY_REPORT_PHASE2.md`](SECURITY_REPORT_PHASE2.md)
- Swagger/collection: `/docs` e `/openapi.json`

## Dados da entrega

- Participante: **Yasmin Luna**
- Repositório: https://github.com/YasminLuna/fiap_cha
- Vídeo: **PREENCHER LINK DO YOUTUBE/VIMEO**
- Usuário avaliador: `soat-architecture`
