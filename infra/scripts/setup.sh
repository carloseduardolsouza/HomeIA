#!/usr/bin/env bash
# Inicializa toda a infra local
# Uso: ./infra/scripts/setup.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f ".env" ]; then
  echo "Copiando .env.example para .env..."
  cp .env.example .env
fi

echo "Subindo infraestrutura..."
docker compose -f infra/compose/docker-compose.dev.yml up -d

echo "Aguardando servicos ficarem saudaveis (timeout: 5 min)..."
end=$((SECONDS+300))
while [ $SECONDS -lt $end ]; do
  healthy_count=$(docker compose -f infra/compose/docker-compose.dev.yml ps | grep -c "(healthy)" || true)
  unhealthy_count=$(docker compose -f infra/compose/docker-compose.dev.yml ps | grep -c "unhealthy" || true)

  if [ "$healthy_count" -ge 9 ]; then
    break
  fi

  if [ "$unhealthy_count" -gt 0 ]; then
    echo "Detectado servico unhealthy. Verifique: docker compose -f infra/compose/docker-compose.dev.yml ps"
    exit 1
  fi

  sleep 5
done

if [ "$healthy_count" -lt 9 ]; then
  echo "Timeout aguardando todos os servicos saudaveis."
  docker compose -f infra/compose/docker-compose.dev.yml ps
  exit 1
fi

bash infra/scripts/init-influxdb.sh
bash infra/scripts/import-grafana-dashboards.sh

echo "Infraestrutura pronta"
echo "Grafana:    http://localhost:${GRAFANA_PORT:-3000}"
echo "InfluxDB:   http://localhost:${INFLUXDB_PORT:-8086}"
echo "Node-RED:   http://localhost:${NODERED_PORT:-1880}"
echo "MLflow:     http://localhost:${MLFLOW_PORT:-5000}"
echo "MinIO API:  http://localhost:${MINIO_API_PORT:-9000}"
echo "MinIO UI:   http://localhost:${MINIO_CONSOLE_PORT:-9002}"

