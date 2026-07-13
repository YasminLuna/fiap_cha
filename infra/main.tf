resource "kind_cluster" "this" {
  name = var.cluster_name
  node_image = "kindest/node:v1.32.2"
  kind_config {kind="Cluster" api_version="kind.x-k8s.io/v1alpha4" node {role="control-plane"} node {role="worker"} node {role="worker"}}
}
provider "kubernetes" {config_path = kind_cluster.this.kubeconfig_path}
resource "kubernetes_namespace_v1" "oficina" {metadata {name="oficina"} depends_on=[kind_cluster.this]}
resource "kubernetes_secret_v1" "postgres" {
  metadata {name="postgres-secret" namespace=kubernetes_namespace_v1.oficina.metadata[0].name}
  data = {POSTGRES_DB="oficina", POSTGRES_USER="oficina", POSTGRES_PASSWORD=var.postgres_password}
}
resource "kubernetes_deployment_v1" "postgres" {
  metadata {name="postgres" namespace=kubernetes_namespace_v1.oficina.metadata[0].name labels={app="postgres"}}
  spec {replicas=1 selector {match_labels={app="postgres"}} template {metadata {labels={app="postgres"}} spec {container {name="postgres" image="postgres:17-alpine" port {container_port=5432} env_from {secret_ref {name=kubernetes_secret_v1.postgres.metadata[0].name}} resources {requests={cpu="100m",memory="128Mi"} limits={cpu="500m",memory="512Mi"}} volume_mount {name="data" mount_path="/var/lib/postgresql/data"}} volume {name="data" empty_dir {}}}}}
}
resource "kubernetes_service_v1" "postgres" {
  metadata {name="postgres" namespace=kubernetes_namespace_v1.oficina.metadata[0].name}
  spec {selector={app="postgres"} port {port=5432 target_port=5432}}
}
