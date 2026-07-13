# Evolução em relação à Fase 1

## Estrutura anterior

A Fase 1 concentrava modelos, serviços e rotas em uma divisão convencional por camadas técnicas.

## Estrutura atual

A organização foi revisada para explicitar responsabilidades:

- `domain`: regras que não dependem de framework;
- `application`: casos de uso da oficina;
- `infrastructure`: persistência, segurança e notificação;
- `presentation`: API e contratos HTTP.

## Principais mudanças

- regras de transição de status centralizadas;
- aprovação e recusa de orçamento tratadas como caso de uso;
- fila operacional ordenada conforme o enunciado da Fase 2;
- exclusão lógica das ordens encerradas;
- endpoints de saúde, prontidão e métricas;
- testes reorganizados para domínio e API;
- preparação para Kubernetes, Terraform e CI/CD.

Essa refatoração reduz duplicação e facilita testar as regras críticas sem depender do ambiente completo.
