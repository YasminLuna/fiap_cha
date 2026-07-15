# Sistema Integrado de Gestão para Oficina Mecânica

## Tech Challenge – Fase II

**Aluno:** Yasmin Luna

**Curso:** Software Architecture – FIAP

**Repositório:** https://github.com/YasminLuna/fiap_cha

---

# Descrição da solução

Este projeto consiste no desenvolvimento de uma API REST para gerenciamento de Ordens de Serviço de uma oficina mecânica.

A solução foi construída utilizando Clean Architecture e princípios de Domain-Driven Design (DDD), permitindo baixo acoplamento entre as camadas da aplicação e facilitando sua evolução.

Além da implementação da API, o projeto contempla a conteinerização da aplicação, orquestração com Kubernetes, provisionamento de infraestrutura utilizando Terraform e automação do processo de integração e entrega contínua por meio do GitHub Actions.

---

# Arquitetura da solução

A aplicação foi organizada seguindo o padrão **Clean Architecture**, separando claramente as responsabilidades em quatro camadas principais.

```text
Cliente
    │
    ▼
FastAPI (Presentation)
    │
    ▼
Use Cases (Application)
    │
    ▼
Domain
    │
    ▼
Infrastructure
    │
    ▼
PostgreSQL
```

## Estrutura do projeto

```text
app/
├── application
├── domain
├── infrastructure
├── presentation
└── main.py

tests/

k8s/

infra/

docs/

.github/
```

---

# Tecnologias utilizadas

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- Kubernetes
- Minikube
- Terraform
- GitHub Actions
- Pytest
- Ruff
- Bandit

---

# Funcionalidades

A API disponibiliza as seguintes funcionalidades:

- Cadastro de Ordem de Serviço
- Consulta de Ordem de Serviço
- Aprovação de orçamento
- Recusa de orçamento
- Atualização de status
- Listagem das Ordens de Serviço
- Health Check
- Readiness Check

---

# Como executar

## Clonar o projeto

```bash
git clone https://github.com/YasminLuna/fiap_cha.git

cd fiap_cha
```

---

## Configurar as variáveis

Criar o arquivo:

```
.env
```

Exemplo:

```env
POSTGRES_DB=oficina_db
POSTGRES_USER=oficina
POSTGRES_PASSWORD=oficina

DATABASE_URL=postgresql+psycopg://oficina:oficina@db:5432/oficina_db

SECRET_KEY=alterar-em-producao

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Executar com Docker Compose

```bash
docker compose up --build
```

A aplicação ficará disponível em:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

Health Check:

```
http://localhost:8000/health
```

---

# Deploy Kubernetes

Iniciar o Minikube

```bash
minikube start
```

Aplicar os manifestos

```bash
kubectl apply -k k8s/
```

Consultar os recursos

```bash
kubectl get all -n oficina
```

---

# Deploy com Terraform

Entrar na pasta

```bash
cd infra
```

Inicializar

```bash
terraform init
```

Validar

```bash
terraform validate
```

Executar o plano

```bash
terraform plan
```

Aplicar

```bash
terraform apply
```

---

# Pipeline CI/CD

A pipeline automatiza as seguintes etapas:

- Checkout do código
- Instalação das dependências
- Execução do Ruff
- Execução dos testes
- Cálculo da cobertura
- Bandit
- Build da imagem Docker
- Publicação da imagem
- Deploy da infraestrutura
- Deploy da aplicação
- Smoke Tests

---

# Testes

Executar:

```bash
pytest
```

Cobertura:

```bash
pytest --cov=app --cov-report=html
```

---

# Segurança

Foram adotadas as seguintes práticas:

- JWT
- Secrets do Kubernetes
- ConfigMaps
- NetworkPolicy
- Containers sem privilégios
- Readiness Probe
- Liveness Probe
- Validação de entrada utilizando Pydantic

---

# Documentação da API

Swagger:

```
http://localhost:8000/docs
```

OpenAPI:

```
http://localhost:8000/openapi.json
```

---

# Vídeo de demonstração

Link:

```
Adicionar após a publicação.
```

---

# Autor

Yasmin Luna

Software Architecture – FIAP

2026