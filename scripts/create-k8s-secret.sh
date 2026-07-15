#!/usr/bin/env sh
set -eu

NAMESPACE="${NAMESPACE:-oficina}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-oficina-local}"
JWT_SECRET="${JWT_SECRET:-change-this-development-secret-with-32-characters}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@oficina.example.com}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-Admin123!}"

kubectl apply -f k8s/namespace.yaml
kubectl -n "$NAMESPACE" create secret generic oficina-secrets \
  --from-literal="DATABASE_URL=postgresql+psycopg://oficina:${POSTGRES_PASSWORD}@postgres:5432/oficina" \
  --from-literal="POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" \
  --from-literal="JWT_SECRET=${JWT_SECRET}" \
  --from-literal="ADMIN_EMAIL=${ADMIN_EMAIL}" \
  --from-literal="ADMIN_PASSWORD=${ADMIN_PASSWORD}" \
  --dry-run=client -o yaml | kubectl apply -f -
