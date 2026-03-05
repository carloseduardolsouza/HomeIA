# Setup Local da Infraestrutura (Entrega 02)

## Pre-requisitos

- Docker 26+
- Docker Compose v2+
- Minimo recomendado: 8 GB RAM livres e 15 GB de disco

## Subindo do zero

1. Na raiz do repositorio, crie o ambiente: `cp .env.example .env`.
2. Ajuste credenciais no `.env`.
3. Rode: `bash infra/scripts/setup.sh`.
4. Verifique estado: `docker compose -f infra/compose/docker-compose.dev.yml ps`.

## Saude dos servicos

Use:

- `docker compose -f infra/compose/docker-compose.dev.yml ps`
- `docker inspect ia-grafana --format '{{json .State.Health}}'`

## Portas e credenciais (dev)

| Servico       | Porta(s)                                               | Credencial padrao                               |
| ------------- | ------------------------------------------------------ | ----------------------------------------------- |
| Mosquitto     | `${MQTT_PORT}` e `${MQTT_WS_PORT}` (default 1883/9001) | `MQTT_USER` / `MQTT_PASSWORD`                   |
| InfluxDB      | `${INFLUXDB_PORT}` (default 8086)                      | `INFLUXDB_USER` / `INFLUXDB_PASSWORD`           |
| PostgreSQL    | `${POSTGRES_PORT}` (default 5432)                      | `POSTGRES_USER` / `POSTGRES_PASSWORD`           |
| Redis         | `${REDIS_PORT}` (default 6379)                         | sem senha (dev)                                 |
| Grafana       | `${GRAFANA_PORT}` (default 3000)                       | `GRAFANA_ADMIN_USER` / `GRAFANA_ADMIN_PASSWORD` |
| Prometheus    | `${PROMETHEUS_PORT}` (default 9090)                    | sem auth (dev)                                  |
| MLflow        | `${MLFLOW_PORT}` (default 5000)                        | sem auth (dev)                                  |
| MinIO API     | `${MINIO_API_PORT}` (default 9000)                     | `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`       |
| MinIO Console | `${MINIO_CONSOLE_PORT}` (default 9002)                 | `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`       |
| Node-RED      | `${NODERED_PORT}` (default 1880)                       | sem auth (dev)                                  |

## Troubleshooting

- Porta ocupada: troque o bind no `infra/compose/docker-compose.dev.yml`.
- Container unhealthy: veja logs com `docker logs <container>`.
- Grafana sem dashboards: confirme mount em `infra/configs/grafana/dashboards/`.
- Mosquitto sem autenticar: valide `infra/configs/mosquitto/passwd` e variaveis MQTT no `.env`.

## Reset completo

1. `docker compose -f infra/compose/docker-compose.dev.yml down -v`
2. `docker volume prune -f` (cuidado: remove volumes nao usados)
3. Suba novamente com `bash infra/scripts/setup.sh`
