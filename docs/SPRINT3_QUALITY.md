# Sprint 3 — Qualidade de Software

Esta sprint consolida a estratégia de qualidade da aplicação da oficina. O foco não foi apenas elevar o percentual de cobertura, mas proteger os fluxos que representam maior risco operacional: abertura da ordem de serviço, movimentação de estoque, transições de status, aprovação do orçamento, ordenação da fila e notificações ao cliente.

## Estratégia de testes

Os testes foram separados em dois grupos:

- **Domínio:** validação de CPF/CNPJ, placa e transições de status.
- **Integração:** execução das APIs com banco SQLite isolado para cada teste.

A suíte utiliza fixtures para preparar o banco, autenticação e catálogo. As factories geram dados válidos e independentes, evitando repetição e acoplamento entre cenários. A integração de notificação é substituída por mock, permitindo verificar chamadas sem depender de servidor SMTP.

## Critérios de qualidade

- Cobertura mínima obrigatória no projeto: **85%**.
- Cobertura de branches habilitada.
- Relatórios gerados em terminal, HTML e XML.
- Ruff usado para lint e formatação.
- Bandit usado para análise estática de segurança.
- Testes executados em banco descartável, sem reutilização de estado.

## Comandos

```bash
make install
make lint
make test
make coverage
make security
make quality
```

O relatório HTML de cobertura é gerado em `htmlcov/index.html`. O arquivo `coverage.xml` pode ser consumido pela pipeline de CI/CD.

## Decisões de Clean Code

- Dados de teste centralizados em factories.
- Preparação de contexto centralizada em fixtures.
- Funções auxiliares de teste nomeadas conforme a intenção do fluxo.
- Cenários pequenos, independentes e com uma razão principal para falhar.
- Mocks limitados às fronteiras externas da aplicação.
