# Documento de entrega - Tech Challenge Fase 2

## Identificação

- Participante: Yasmin Luna
- Repositório: https://github.com/YasminLuna/fiap_cha
- Usuário avaliador: `soat-architecture`
- Vídeo: PREENCHER APÓS PUBLICAÇÃO NO YOUTUBE OU VIMEO

## Solução entregue

A aplicação da Fase 1 foi evoluída para um monólito modular orientado pela Clean Architecture. O domínio de ordens de serviço permanece isolado das dependências de HTTP, persistência, autenticação e notificação. A solução inclui PostgreSQL, Docker, Kubernetes com HPA, infraestrutura local provisionada por Terraform e pipeline de CI/CD no GitHub Actions.

## Evidências

- Swagger: `/docs`
- OpenAPI: `/openapi.json`
- Testes: cobertura mínima configurada em 80%; execução validada com 90,57%
- Kubernetes: Deployment, Service, ConfigMap, Secret, PostgreSQL, PVC, HPA e NetworkPolicy
- Terraform: cluster Kind e PostgreSQL
- CI/CD: lint, testes, cobertura, Bandit, build/push da imagem, Trivy, deploy e smoke test

## Pendência antes do envio

Inserir somente o link do vídeo após a gravação e conferir que o repositório foi compartilhado com `soat-architecture`.
