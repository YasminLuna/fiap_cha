# Infraestrutura local com Terraform

Este módulo cria um cluster Kubernetes local Kind com um control-plane e dois workers. Em seguida, cria o namespace `oficina`, o Secret do PostgreSQL, o Deployment do banco e seu Service interno.

```bash
cd infra
terraform init
terraform plan
terraform apply
```

O banco usa `emptyDir` apenas para demonstração acadêmica local. Em cloud, deve ser substituído por serviço gerenciado ou PersistentVolume adequado.
