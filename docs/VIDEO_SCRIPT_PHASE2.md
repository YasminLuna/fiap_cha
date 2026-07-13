# Roteiro do vídeo — até 15 minutos

1. **Contexto e arquitetura (1min30):** evolução da Fase 1, Clean Architecture e componentes do diagrama.
2. **Código e testes (2min):** estrutura, regra de transição de status e `pytest` com cobertura.
3. **Execução local (2min):** `docker compose up --build`, `/health`, `/docs` e autenticação.
4. **Fluxo funcional (3min):** criar cliente, veículo, serviço e peça; abrir OS; diagnóstico; aguardando aprovação; aprovar orçamento; consultar status e listagem priorizada.
5. **CI/CD (2min):** abrir GitHub Actions e explicar lint, testes, imagem, Trivy e deploy.
6. **Terraform e Kubernetes (2min):** `terraform plan`, `kubectl get pods,svc,hpa -n oficina` e probes.
7. **HPA (1min30):** executar `scripts/load-test.sh`, acompanhar `kubectl get hpa -w` e mostrar aumento de réplicas.
8. **Encerramento (30s):** principais decisões e limitações do MVP.
