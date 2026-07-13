# Modelo de domínio

## Linguagem ubíqua

| Termo | Definição utilizada no projeto |
|---|---|
| Ordem de Serviço (OS) | Registro que reúne cliente, veículo, serviços, peças, orçamento e andamento do atendimento. |
| Diagnóstico | Etapa em que a oficina avalia o veículo e confirma os itens necessários. |
| Orçamento | Soma dos serviços e peças associados à ordem de serviço. |
| Aprovação | Resposta externa do cliente autorizando a execução do orçamento. |
| Fila operacional | Relação de ordens ainda ativas, ordenadas por prioridade e antiguidade. |
| Entrega | Encerramento do fluxo após a finalização e devolução do veículo. |

## Entidades principais

### Cliente

- identificador;
- nome;
- CPF ou CNPJ;
- e-mail;
- telefone.

### Veículo

- identificador;
- cliente proprietário;
- placa;
- marca;
- modelo;
- ano.

### Serviço

- identificador;
- descrição;
- valor;
- tempo estimado.

### Peça

- identificador;
- descrição;
- valor unitário;
- quantidade em estoque.

### Ordem de Serviço

É o agregado central do domínio. Mantém o vínculo com cliente e veículo, os serviços e peças selecionados, o orçamento calculado, o status atual e as datas do fluxo.

## Invariantes

- A OS deve possuir cliente e veículo válidos.
- Uma alteração de status deve respeitar o fluxo definido.
- Apenas uma OS aguardando aprovação pode receber aprovação ou recusa.
- Uma OS finalizada, entregue ou cancelada não aparece na fila operacional.
- Dentro da mesma prioridade, a ordem mais antiga deve aparecer primeiro.
- A recusa do orçamento encerra o fluxo como cancelado.

## Casos de uso

### Abrir ordem de serviço

Recebe os dados necessários, calcula o valor dos itens e retorna o identificador único da OS.

### Consultar status

Retorna a situação atual e os principais dados de acompanhamento.

### Responder orçamento

Processa aprovação ou recusa recebida por endpoint externo.

### Atualizar status

Valida a transição, persiste a mudança e dispara uma notificação.

### Listar fila operacional

Exclui ordens encerradas e aplica prioridade por status e data de criação.
