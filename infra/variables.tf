variable "kubernetes_context" {
  description = "Contexto Kubernetes utilizado pelo Terraform"
  type        = string
  default     = "minikube"
}

variable "namespace" {
  description = "Namespace da aplicação"
  type        = string
  default     = "oficina"
}

variable "access_token_expire_minutes" {
  description = "Tempo de expiração do token JWT"
  type        = number
  default     = 60
}

variable "database_url" {
  description = "URL de conexão da aplicação com o PostgreSQL"
  type        = string
  sensitive   = true
  default     = "postgresql+psycopg://oficina:oficina@postgres:5432/oficina_db"
}

variable "secret_key" {
  description = "Chave utilizada para assinatura dos tokens JWT"
  type        = string
  sensitive   = true
}

variable "postgres_database" {
  description = "Nome do banco PostgreSQL"
  type        = string
  default     = "oficina_db"
}

variable "postgres_user" {
  description = "Usuário do PostgreSQL"
  type        = string
  default     = "oficina"
}

variable "postgres_password" {
  description = "Senha do PostgreSQL"
  type        = string
  sensitive   = true
}

variable "postgres_storage" {
  description = "Capacidade do volume persistente"
  type        = string
  default     = "1Gi"
}