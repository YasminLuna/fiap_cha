output "cluster_name" {value=kind_cluster.this.name}
output "kubeconfig_path" {value=kind_cluster.this.kubeconfig_path}
output "database_service" {value="postgres.oficina.svc.cluster.local:5432"}
