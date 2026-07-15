# Fluxo CI/CD

```mermaid
graph LR
Push-->GitHub_Actions
GitHub_Actions-->Testes
Testes-->Build_Docker
Build_Docker-->Terraform
Terraform-->Kubernetes
Kubernetes-->Smoke_Tests
```
