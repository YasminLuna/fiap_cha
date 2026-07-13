# Sistema Integrado de Atendimento e Execução de Serviços - Oficina Mecânica

## 1. Objetivo

Este projeto foi desenvolvido como MVP de back-end para uma oficina mecânica de médio porte. A proposta é organizar o atendimento, diagnóstico, orçamento, execução e entrega dos veículos, substituindo controles manuais por uma API estruturada, segura e documentada.

O sistema permite cadastrar clientes, veículos, serviços, peças, controlar estoque, criar ordens de serviço, gerar orçamento automaticamente e acompanhar o status da OS.

## 2. Stack escolhida

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Swagger automático
- Docker e Docker Compose
- Pytest
- Bandit para análise de vulnerabilidades

## 3. Justificativa da stack

A escolha do FastAPI foi feita por sua curva de aprendizado simples, produtividade e documentação automática via Swagger. Para um MVP, isso reduz complexidade sem comprometer a qualidade técnica. O PostgreSQL foi escolhido por ser um banco relacional robusto e adequado para dados que exigem consistência, como clientes, veículos, ordens de serviço, orçamento, peças e movimentação de estoque.

## 4. Arquitetura

O projeto segue uma arquitetura monolítica em camadas:

```text
app/
  api/        -> rotas REST
  core/       -> configurações e segurança
  db/         -> conexão com banco
  domain/     -> modelos de domínio
  schemas/    -> contratos de entrada e saída
  services/   -> regras de negócio
```

## 5. Como executar localmente

### Usando Docker

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Login administrativo

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Endpoint:

```text
POST /auth/login
```

## 6. Principais endpoints

### Autenticação

- `POST /auth/login`

### Clientes

- `POST /clientes`
- `GET /clientes`

### Veículos

- `POST /veiculos`
- `GET /veiculos`

### Serviços

- `POST /servicos`
- `GET /servicos`

### Peças

- `POST /pecas`
- `GET /pecas`

### Ordens de Serviço

- `POST /ordens-servico`
- `GET /ordens-servico`
- `GET /ordens-servico/{id}`
- `PATCH /ordens-servico/{id}/status`

### Métricas

- `GET /metricas/tempo-medio-execucao`

## 7. Fluxo principal da OS

1. Cliente e veículo são cadastrados.
2. Serviços e peças são cadastrados.
3. A ordem de serviço é aberta com serviços e peças necessárias.
4. O sistema calcula automaticamente o valor total.
5. O status inicial da OS fica como `Aguardando aprovação`.
6. Após aprovação, a OS pode seguir para `Em execução`.
7. Ao concluir o serviço, o status muda para `Finalizada`.
8. Após retirada do veículo, a OS muda para `Entregue`.

## 8. Status disponíveis

- Recebida
- Em diagnóstico
- Aguardando aprovação
- Em execução
- Finalizada
- Entregue

## 9. Testes

Executar testes:

```bash
pytest
```

Executar testes com cobertura:

```bash
coverage run -m pytest
coverage report
```

## 10. Análise de vulnerabilidades

Executar Bandit:

```bash
bandit -r app
```

## 11. Observações de segurança

- APIs administrativas protegidas por JWT.
- Validação de CPF/CNPJ por quantidade de dígitos.
- Validação de placa no padrão brasileiro/Mercosul.
- Senha administrativa fixa apenas para MVP. Em produção, deve ser substituída por usuários persistidos no banco com hash de senha.
