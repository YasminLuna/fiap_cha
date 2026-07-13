# Roteiro para vídeo de apresentação - até 15 minutos

## 1. Abertura

Olá, meu nome é Yasmin Luna e esta é a apresentação do Tech Challenge Fase 1. O projeto desenvolvido é um MVP de back-end para uma oficina mecânica de médio porte, com foco em gestão de ordens de serviço, clientes, veículos, peças e acompanhamento do status dos serviços.

## 2. Problema

A oficina tinha um processo desorganizado, baseado em planilhas e anotações manuais. Isso gerava erros na priorização dos atendimentos, dificuldade no controle de peças, falta de histórico dos clientes e pouca visibilidade sobre o andamento das ordens de serviço.

## 3. Solução proposta

A solução foi criar uma API back-end que centraliza o cadastro de clientes, veículos, serviços e peças, além de permitir a criação e acompanhamento de ordens de serviço. O sistema calcula o orçamento automaticamente e permite acompanhar os status da OS.

## 4. Stack

Foi utilizado Python com FastAPI, PostgreSQL, SQLAlchemy, JWT, Docker, Pytest e documentação automática via Swagger.

## 5. DDD

Na modelagem DDD, foram identificados os contextos de Atendimento, Execução de Serviços, Estoque e Administrativo. A Ordem de Serviço foi definida como o principal agregado do sistema, pois concentra cliente, veículo, serviços, peças, status e orçamento.

## 6. Demonstração da API

Mostrar no Swagger:

1. Login em `/auth/login`.
2. Cadastro de cliente.
3. Cadastro de veículo.
4. Cadastro de serviço.
5. Cadastro de peça.
6. Criação da ordem de serviço.
7. Consulta da ordem de serviço.
8. Alteração de status.
9. Consulta da métrica de tempo médio.

## 7. Segurança

Explicar que as APIs administrativas usam JWT e que foram implementadas validações para CPF/CNPJ e placa. Também comentar o relatório de vulnerabilidades e os pontos de melhoria para produção.

## 8. Testes e Docker

Mostrar a execução do Docker Compose e dos testes com Pytest. Explicar que o projeto foi preparado para execução local simples.

## 9. Encerramento

Concluir dizendo que o MVP atende aos principais requisitos da fase, com uma arquitetura simples, organizada e evolutiva para futuras funcionalidades, como aplicativo do cliente, aprovação de orçamento em tempo real e controle mais avançado de estoque.
