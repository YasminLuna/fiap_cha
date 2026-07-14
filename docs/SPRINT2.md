# Registro da Sprint 2

A Sprint 2 concentrou a evolução operacional da solução. A aplicação validada na sprint anterior passou a ser empacotada em uma imagem imutável e executada com dependências e configurações externas ao código.

## Decisões principais

O Kubernetes foi adotado para suportar replicação, probes de saúde e escalabilidade horizontal. O PostgreSQL permanece no mesmo cluster apenas para fins acadêmicos e de execução local. Em um cenário produtivo, a recomendação seria utilizar um serviço gerenciado de banco de dados.

O Terraform cria o ambiente local com Kind e provisiona o banco. Os manifestos em `k8s/` descrevem a aplicação e permitem que o mesmo artefato seja aplicado manualmente ou pela pipeline.

A pipeline separa qualidade, validação da infraestrutura, imagem e deploy. Dessa forma, uma falha nos testes, no Terraform ou no scan de vulnerabilidades interrompe a entrega antes da implantação.

## Relação com os requisitos

- Dockerfile e Docker Compose revisados.
- Deployment, Service, ConfigMap, Secret, PostgreSQL e HPA.
- Infraestrutura como código com Terraform.
- Pipeline com build, testes, imagem, banco, Kubernetes e smoke test.
- Demonstração de escalabilidade por meio do script de carga.
