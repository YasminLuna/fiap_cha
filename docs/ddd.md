# Domain Driven Design

## Linguagem Ubíqua
- Cliente
- Veículo
- Ordem de Serviço
- Orçamento
- Peça
- Serviço

## Fluxo

```mermaid
graph LR
Recebida-->Diagnóstico
Diagnóstico-->Aguardando_Aprovação
Aguardando_Aprovação-->Execução
Execução-->Finalizada
Finalizada-->Entregue
```
