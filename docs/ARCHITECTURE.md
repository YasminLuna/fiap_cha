# Arquitetura

## Estilo
Clean Architecture.

## Camadas
- Presentation
- Application
- Domain
- Infrastructure

## Fluxo

```mermaid
graph TD
Cliente-->API
API-->Application
Application-->Domain
Application-->Infrastructure
Infrastructure-->PostgreSQL
```
