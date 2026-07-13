# Documento de Entrega - Tech Challenge Fase 1

## 1. Nome do Projeto

Sistema Integrado de Atendimento e Execução de Serviços para Oficina Mecânica

## 2. Grupo

Entrega individual

## 3. Participante

Yasmin Luna

## 4. Username no Discord

Preencher com o username utilizado no Discord.

## 5. Link da documentação DDD

Preencher com o link do Miro, FigJam ou documento equivalente.

## 6. Link do repositório

Preencher com o link do repositório privado concedendo acesso ao usuário `soat-architecture`.

## 7. Resumo da solução

O projeto consiste em um MVP de back-end para uma oficina mecânica de médio porte. A solução organiza o fluxo de atendimento, criação da Ordem de Serviço, controle de peças, cálculo de orçamento, aprovação e acompanhamento do status do serviço.

A aplicação foi desenvolvida como um monolito em camadas, utilizando Python com FastAPI e PostgreSQL. Essa abordagem foi escolhida por facilitar a entrega do MVP, manter o código simples de entender e permitir uma evolução futura mais organizada.

## 8. Funcionalidades entregues

- Cadastro e listagem de clientes.
- Cadastro e listagem de veículos.
- Cadastro e listagem de serviços.
- Cadastro e listagem de peças e insumos.
- Controle básico de estoque.
- Criação de Ordem de Serviço.
- Cálculo automático de orçamento.
- Alteração de status da OS.
- Consulta pública do andamento da OS.
- Métrica de tempo médio de execução.
- Autenticação JWT para APIs administrativas.
- Documentação automática via Swagger.
- Dockerfile e docker-compose.
- Testes automatizados.
- Relatório de vulnerabilidades.

## 9. Stack técnica

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pytest
- Docker
- Docker Compose
- Bandit

## 10. Justificativa do banco de dados

O PostgreSQL foi escolhido por ser um banco relacional robusto, estável e adequado para dados estruturados. O domínio da oficina possui relacionamentos claros entre cliente, veículo, ordem de serviço, serviços e peças. Por isso, um banco relacional facilita a integridade, consistência e rastreabilidade das informações.

## 11. Arquitetura utilizada

A arquitetura adotada foi um monolito em camadas, dividindo responsabilidades entre API, domínio, schemas, serviços, segurança e banco de dados.

Essa escolha é adequada para um MVP porque reduz complexidade operacional, facilita a execução local e mantém o projeto simples para apresentação e manutenção.

## 12. Segurança

As APIs administrativas são protegidas por autenticação JWT. Também foram implementadas validações de dados sensíveis, como CPF/CNPJ e placa de veículo.

O relatório de vulnerabilidades aponta melhorias necessárias antes de produção, como remover credenciais fixas, exigir SECRET_KEY forte e implementar perfis de acesso.

## 13. Testes

Foram criados testes automatizados para healthcheck, autenticação e validações principais. A proposta é manter cobertura mínima de 80% nos domínios críticos do sistema, principalmente criação de OS, validação de entrada, controle de estoque e mudança de status.

## 14. Conclusão

A solução entregue atende à proposta do Tech Challenge ao implementar um MVP funcional para gestão de oficina mecânica, aplicando DDD, arquitetura em camadas, autenticação, documentação de APIs, Docker, testes e análise de vulnerabilidades.
