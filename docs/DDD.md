# Documentação DDD - Sistema de Oficina Mecânica

## 1. Visão do domínio

O domínio representa o processo de atendimento de uma oficina mecânica, desde a chegada do cliente até a entrega do veículo. O problema central é organizar o fluxo de atendimento, orçamento, aprovação, execução e controle de peças, reduzindo falhas manuais e aumentando a rastreabilidade.

## 2. Linguagem Ubíqua

| Termo | Significado |
|---|---|
| Cliente | Pessoa física ou jurídica que solicita atendimento |
| Veículo | Automóvel vinculado a um cliente |
| Ordem de Serviço | Registro principal do atendimento de um veículo |
| Serviço | Atividade executada pela oficina, como troca de óleo ou alinhamento |
| Peça/Insumo | Item utilizado na execução do serviço |
| Orçamento | Valor calculado com base nos serviços e peças da OS |
| Aprovação | Confirmação do cliente para início ou continuidade do reparo |
| Status da OS | Etapa atual do fluxo de atendimento |
| Estoque | Quantidade disponível de peças e insumos |
| Tempo Médio de Execução | Indicador administrativo do tempo gasto na execução dos serviços |

## 3. Bounded Contexts

### Atendimento

Responsável por clientes, veículos e abertura da Ordem de Serviço.

### Execução de Serviços

Responsável pelo acompanhamento da OS, mudança de status e finalização.

### Estoque

Responsável pelas peças, insumos e controle de quantidade disponível.

### Administrativo

Responsável por cadastros, listagem de OS e métricas de tempo médio.

## 4. Agregados

### Cliente

Entidade raiz para os dados cadastrais do cliente.

### Veículo

Entidade associada ao cliente. Um cliente pode possuir vários veículos.

### Ordem de Serviço

Principal agregado do sistema. Controla serviços solicitados, peças utilizadas, orçamento, status e datas relevantes.

### Peça

Entidade responsável por preço, código e quantidade em estoque.

### Serviço

Entidade responsável pelo nome, descrição, preço e tempo estimado.

## 5. Value Objects

- CPF/CNPJ
- Placa
- Status da Ordem de Serviço
- Valor monetário
- Quantidade de estoque

## 6. Entidades principais

### Cliente

Atributos:

- id
- nome
- documento
- telefone
- email

### Veículo

Atributos:

- id
- placa
- marca
- modelo
- ano
- cliente_id

### Serviço

Atributos:

- id
- nome
- descrição
- preço
- tempo estimado

### Peça

Atributos:

- id
- nome
- código
- preço
- quantidade em estoque

### Ordem de Serviço

Atributos:

- id
- cliente_id
- veículo_id
- status
- observação
- valor total
- data de criação
- data de início
- data de finalização

## 7. Regras de negócio

1. Uma OS deve estar associada a um cliente e a um veículo.
2. Uma OS pode conter um ou mais serviços.
3. Uma OS pode conter peças e insumos.
4. O orçamento é calculado automaticamente a partir da soma dos serviços e peças.
5. O sistema não permite uso de peça com estoque insuficiente.
6. Ao incluir peça em uma OS, a quantidade é abatida do estoque.
7. O cliente pode consultar o status da OS por API.
8. Apenas usuários administrativos autenticados podem criar, alterar e listar dados internos.
9. Ao mudar o status para `Em execução`, o sistema registra o início.
10. Ao mudar o status para `Finalizada`, o sistema registra a conclusão.

## 8. Event Storming - Criação e acompanhamento da OS

### Eventos de domínio

- Cliente identificado
- Veículo cadastrado
- Serviços solicitados registrados
- Peças necessárias incluídas
- Estoque validado
- Orçamento calculado
- Orçamento enviado para aprovação
- Orçamento aprovado pelo cliente
- Ordem de serviço colocada em execução
- Serviço finalizado
- Veículo entregue

### Comandos

- Identificar cliente
- Cadastrar veículo
- Criar ordem de serviço
- Adicionar serviço à OS
- Adicionar peça à OS
- Calcular orçamento
- Alterar status da OS
- Consultar andamento da OS

### Políticas

- Se houver estoque insuficiente, a OS não pode reservar a peça.
- Se o orçamento for aprovado, a OS pode entrar em execução.
- Se a execução for concluída, a OS pode ser finalizada.
- Se o veículo for retirado pelo cliente, a OS pode ser entregue.

## 9. Event Storming - Gestão de peças e insumos

### Eventos de domínio

- Peça cadastrada
- Estoque atualizado
- Peça associada à OS
- Estoque debitado
- Estoque insuficiente identificado

### Comandos

- Cadastrar peça
- Atualizar estoque
- Consultar peça
- Reservar peça para OS

### Políticas

- Peças devem possuir código único.
- Peças não podem ter estoque negativo.
- A OS só pode consumir peças disponíveis.

## 10. Diagrama textual do fluxo da OS

```text
Cliente chega na oficina
        ↓
Cliente é identificado por CPF/CNPJ
        ↓
Veículo é cadastrado ou localizado
        ↓
Serviços solicitados são informados
        ↓
Peças e insumos são adicionados
        ↓
Sistema valida estoque
        ↓
Sistema calcula orçamento
        ↓
OS fica aguardando aprovação
        ↓
Cliente aprova
        ↓
OS entra em execução
        ↓
Serviço é finalizado
        ↓
Veículo é entregue
```

## 11. Decisões arquiteturais

Foi adotado um monolito em camadas porque o projeto é um MVP. Essa abordagem facilita entendimento, desenvolvimento, testes e execução local. A separação em camadas evita acoplamento excessivo e permite evolução futura para módulos ou serviços independentes, caso o sistema cresça.
