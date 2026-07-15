output "namespace" {
  description = "Namespace criado para a aplicação"
  value       = kubernetes_namespace_v1.oficina.metadata[0].name
}

output "postgres_secret_name" {
  description = "Nome do Secret do PostgreSQL"
  value       = kubernetes_secret_v1.postgres.metadata[0].name
}

output "postgres_pvc_name" {
  description = "Nome do PVC do PostgreSQL"
  value       = kubernetes_persistent_volume_claim_v1.postgres.metadata[0].name
}

output "postgres_service_name" {
  description = "Nome do Service do PostgreSQL"
  value       = kubernetes_service_v1.postgres.metadata[0].name
}

output "postgres_deployment_name" {
  description = "Nome do Deployment do PostgreSQL"
  value       = kubernetes_deployment_v1.postgres.metadata[0].name
}