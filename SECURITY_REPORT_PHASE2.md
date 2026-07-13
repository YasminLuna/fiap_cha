# Relatório de segurança — Fase 2

## Controles aplicados

- APIs administrativas protegidas por JWT.
- Segredos fora do repositório; o arquivo Kubernetes versionado é apenas exemplo.
- Container executado com usuário sem privilégios e filesystem somente leitura no Kubernetes.
- Validação de CPF/CNPJ, placa, estoque e transições de estado.
- SQLAlchemy com consultas parametrizadas.
- Bandit para análise estática e Trivy para imagem Docker no pipeline.
- NetworkPolicy restringindo comunicação da API.

## Execução dos scans

```bash
bandit -r app -ll
trivy fs --severity HIGH,CRITICAL .
trivy image --severity HIGH,CRITICAL oficina-api:local
```

Os resultados reais devem ser anexados após a execução no repositório definitivo. Achados críticos ou altos bloqueiam o pipeline. Senhas de exemplo são exclusivas do ambiente local e devem ser substituídas por secrets do GitHub ou solução de cofre em ambientes compartilhados.
