# Gateway IoT

Servico responsavel por consumir mensagens MQTT, validar leituras de sensores e persistir dados em InfluxDB/PostgreSQL.
Tambem disponibiliza API HTTP de ingestao e metricas Prometheus.

## Como rodar local

1. Crie e ative um ambiente virtual Python.
2. Instale dependencias: `pip install -r requirements.txt`
3. Execute API + MQTT listener: `uvicorn src.api:app --reload --host 0.0.0.0 --port 8000`
4. Abra docs: `http://localhost:8000/docs`

## Variaveis de ambiente

- `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASSWORD`
- `INFLUXDB_URL`, `INFLUXDB_TOKEN`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET`
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `MQTT_ENABLED` (`true`/`false`, default `true`)
- `INFLUXDB_ENABLED` (`true`/`false`, default `true`)
- `POSTGRES_ENABLED` (`true`/`false`, default `true`)

## Endpoints

- `POST /api/v1/ingest/sensor`
- `POST /api/v1/ingest/batch` (maximo 100 leituras)
- `GET /api/v1/health`
- `GET /metrics`

## Topicos MQTT suportados

- `casa/energia/consumo`
- `casa/energia/disjuntor`
- `casa/energia/medidor/{id_medidor}`
- `jardim/solo/umidade`
- `jardim/solo/temperatura`
- `casa/ambiente/temperatura`

## Testes

- `pytest -q`
- `pytest --cov=src --cov-report=term-missing`
