#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLUSTER_NAME="${CLUSTER_NAME:-oficina}"
IMAGE="oficina-api:local"

"$ROOT_DIR/scripts/kind-up.sh"
docker build -t "$IMAGE" "$ROOT_DIR"
kind load docker-image "$IMAGE" --name "$CLUSTER_NAME"

kubectl apply -f "$ROOT_DIR/k8s/namespace.yaml"
if ! kubectl -n oficina get secret oficina-secrets >/dev/null 2>&1; then
  kubectl -n oficina create secret generic oficina-secrets \
    --from-literal=DATABASE_URL='postgresql+psycopg://oficina:oficina@postgres:5432/oficina' \
    --from-literal=POSTGRES_PASSWORD='oficina' \
    --from-literal=JWT_SECRET='local-secret-with-at-least-32-characters' \
    --from-literal=ADMIN_EMAIL='admin@oficina.local' \
    --from-literal=ADMIN_PASSWORD='Admin123!'
fi

kubectl apply -k "$ROOT_DIR/k8s"
kubectl set image deployment/oficina-api api="$IMAGE" -n oficina
kubectl rollout status deployment/postgres -n oficina --timeout=180s
kubectl rollout status deployment/oficina-api -n oficina --timeout=180s
kubectl get pods,svc,ingress,hpa -n oficina
