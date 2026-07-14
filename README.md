# Sistema Integrado de Gestão para Oficina Mecânica

## Objetivo
Evolução da aplicação da Fase 1 com foco em Clean Architecture, Docker,
Kubernetes, Terraform e CI/CD.

## Tecnologias
- Python
- FastAPI
- PostgreSQL
- Docker
- Kubernetes
- Terraform
- GitHub Actions

## Estrutura
- app/
- tests/
- infra/
- k8s/
- docs/

## Execução
```bash
docker compose up --build
```

## Deploy
1. Provisionar infraestrutura com Terraform.
2. Aplicar manifestos Kubernetes.
3. Pipeline GitHub Actions realiza build, testes e deploy.

## Autor
Yasmin Luna
