# Arquitetura da solução

## Decisão arquitetural

A aplicação evoluiu do monólito em camadas da Fase 1 para um **monólito modular orientado por Clean Architecture**. O domínio contém regras independentes de framework; a camada de aplicação coordena casos de uso; infraestrutura implementa persistência, autenticação e notificações; apresentação expõe a API REST.

```mermaid
flowchart LR
  C[Cliente / Administrativo] --> API[FastAPI REST]
  API --> UC[Casos de uso]
  UC --> D[Domínio e regras]
  UC --> R[SQLAlchemy]
  R --> DB[(PostgreSQL)]
  UC --> N[Notificador SMTP/Log]
  GH[GitHub Actions] --> REG[GHCR]
  GH --> K8S[Kubernetes]
  TF[Terraform] --> K8S
  TF --> DB
```

## Fluxo de deploy

```mermaid
flowchart LR
  P[Push/Merge Request] --> L[Lint]
  L --> T[Testes + cobertura]
  T --> S[Bandit]
  S --> B[Build Docker]
  B --> V[Trivy]
  V --> R[Push GHCR]
  R --> D[Deploy Kubernetes]
  D --> SM[Smoke test /health]
```

## Escalabilidade e resiliência

O Deployment inicia com duas réplicas. O HPA varia entre 2 e 8 réplicas por CPU e memória. Readiness e liveness probes evitam envio de tráfego a pods indisponíveis. Requests e limits tornam o comportamento do HPA previsível.
