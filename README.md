# Oficina API — Fase 2 | Sprint 1

Esta entrega representa a primeira etapa da evolução do Tech Challenge da Fase 1. O foco desta sprint é reorganizar a aplicação com **Clean Architecture**, revisar a modelagem do domínio e deixar os fluxos críticos preparados para as próximas etapas de infraestrutura e automação.

## Escopo desta sprint

- Reorganização da aplicação em domínio, aplicação, infraestrutura e apresentação.
- Revisão das regras de transição de status da ordem de serviço.
- Implementação dos casos de uso centrais da Fase 2.
- Adequação das APIs de abertura, consulta, aprovação e priorização das ordens.
- Modelagem relacional com PostgreSQL e SQLAlchemy.
- Autenticação administrativa por JWT.
- Testes automatizados dos fluxos críticos.
- Documentação da arquitetura e das decisões técnicas.

Os artefatos de Kubernetes, Terraform e CI/CD serão incorporados na etapa seguinte, depois da validação funcional da aplicação.

## Arquitetura

```text
app/
├── domain/          # regras e conceitos de negócio
├── application/     # coordenação dos casos de uso
├── infrastructure/  # banco, segurança e notificação
├── presentation/    # contratos e rotas HTTP
└── main.py
```

A decisão arquitetural está detalhada em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). A modelagem e o vocabulário do domínio estão em [`docs/DOMAIN_MODEL.md`](docs/DOMAIN_MODEL.md).

## Fluxos atendidos

- Abertura de OS com cliente, veículo, serviços e peças.
- Retorno de identificação única da ordem de serviço.
- Consulta do status atual da OS.
- Aprovação ou recusa externa de orçamento.
- Atualização controlada do status da OS.
- Listagem operacional com a prioridade exigida na Fase 2.
- Exclusão lógica de ordens finalizadas, entregues ou canceladas da fila ativa.
- Notificação de alteração de status por SMTP ou registro em log.

## Regra de priorização

A fila operacional é apresentada nesta ordem:

1. Em execução.
2. Aguardando aprovação.
3. Em diagnóstico.
4. Recebida.

Dentro do mesmo status, as ordens mais antigas aparecem primeiro.

## Execução local

```bash
cp .env.example .env
docker compose up --build
```

Acessos locais:

- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`
- Métricas: `http://localhost:8000/metrics`

Credencial administrativa de desenvolvimento:

```text
admin@oficina.example.com
Admin123!
```

## Testes

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

Resultado validado nesta entrega:

```text
5 testes aprovados
90,57% de cobertura
```

A configuração exige cobertura mínima de 80%.

## Próxima etapa

A Sprint 2 adicionará:

- Docker revisado para produção;
- manifestos Kubernetes;
- HPA por CPU e memória;
- infraestrutura em Terraform;
- pipeline GitHub Actions;
- scans de segurança e smoke tests.

## Identificação

- Participante: **Yasmin Luna**
- Repositório: `https://github.com/YasminLuna/fiap_cha`
