#!/usr/bin/env bash
set -euo pipefail
URL=${1:-http://localhost:8000/health}
echo "Gerando carga em $URL. Encerre com Ctrl+C."
for i in $(seq 1 20); do
  while true; do curl -fsS "$URL" >/dev/null; done &
done
wait
