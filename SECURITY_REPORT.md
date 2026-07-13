# Relatório de Análise de Vulnerabilidades

## 1. Objetivo

Este relatório apresenta a análise de vulnerabilidades realizada no MVP do Sistema Integrado de Atendimento e Execução de Serviços para Oficina Mecânica.

A análise considera o código-fonte, dependências principais e pontos sensíveis da aplicação, como autenticação, validação de entrada e exposição de APIs administrativas.

## 2. Ferramenta sugerida

A ferramenta indicada para o scan estático é o Bandit, voltada para análise de vulnerabilidades em aplicações Python.

Comando utilizado:

```bash
bandit -r app
```

## 3. Resultado esperado do scan

Para a versão atual do MVP, a expectativa é não encontrar vulnerabilidades críticas no fluxo principal. Porém, alguns pontos devem ser tratados antes de um ambiente produtivo.

## 4. Vulnerabilidades e riscos identificados

### 4.1 Credencial administrativa fixa

**Severidade:** Média

O login administrativo utiliza usuário e senha fixos para facilitar a demonstração do MVP.

**Risco:** Em produção, credenciais fixas podem permitir acesso indevido caso sejam conhecidas.

**Correção recomendada:** Criar tabela de usuários administrativos, armazenar senhas com hash seguro e permitir gestão de usuários.

### 4.2 SECRET_KEY com valor padrão

**Severidade:** Média

A aplicação possui uma chave padrão para assinatura do JWT caso a variável de ambiente não seja informada.

**Risco:** Tokens podem ser forjados se a chave padrão for usada em produção.

**Correção recomendada:** Exigir SECRET_KEY forte por variável de ambiente e impedir inicialização em produção sem essa configuração.

### 4.3 Validação simplificada de CPF/CNPJ

**Severidade:** Baixa

A validação atual verifica apenas a quantidade de dígitos do CPF/CNPJ.

**Risco:** Documentos com formato correto, mas número inválido, podem ser aceitos.

**Correção recomendada:** Implementar validação completa de dígitos verificadores.

### 4.4 Ausência de controle de perfis

**Severidade:** Baixa

A autenticação protege APIs administrativas, mas ainda não separa perfis como administrador, mecânico e atendente.

**Risco:** Usuários autenticados teriam acesso amplo às funções internas.

**Correção recomendada:** Implementar RBAC com perfis e permissões por endpoint.

### 4.5 Ausência de rate limit

**Severidade:** Baixa

A API não possui limitação de tentativas de login.

**Risco:** Pode permitir tentativas automatizadas de força bruta.

**Correção recomendada:** Adicionar rate limit no endpoint de autenticação.

## 5. Pontos positivos de segurança

- Uso de JWT para proteger APIs administrativas.
- Separação entre endpoints públicos e administrativos.
- Validação de placa de veículo.
- Validação básica de CPF/CNPJ.
- Uso de variáveis de ambiente no Docker Compose.
- Banco de dados isolado em container.

## 6. Plano de melhoria

| Item | Ação | Prioridade |
|---|---|---|
| Credencial fixa | Criar autenticação com usuários no banco e senha com hash | Alta |
| SECRET_KEY | Obrigar chave forte em produção | Alta |
| CPF/CNPJ | Implementar validação completa | Média |
| Perfis de acesso | Criar RBAC | Média |
| Rate limit | Limitar tentativas de login | Média |
| Logs de auditoria | Registrar ações administrativas | Baixa |

## 7. Conclusão

O MVP atende aos requisitos principais de segurança para demonstração acadêmica, especialmente por utilizar JWT e validações de entrada. Para uso produtivo, recomenda-se evoluir autenticação, autorização por perfis, validação documental completa e proteção contra abuso de endpoints.
