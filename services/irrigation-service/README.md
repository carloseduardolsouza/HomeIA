# Irrigation Service

Servico de decisao de irrigacao (a cada 10 min) com regras de negocio RN-10..RN-13,
integracao com OpenWeatherMap e cache Redis.

## Arquivos principais

- `src/decision_engine.py`
- `src/weather_client.py`
- `src/rules/business_rules.py`
- `src/scheduler.py`

## Variaveis de ambiente

- `OPENWEATHER_API_KEY`
- `OPENWEATHER_CITY`
- `REDIS_HOST`, `REDIS_PORT`
- `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASSWORD`

## Execucao

`python -m src.main`

## MQTT

Comando de cancelamento manual:

- topico: `jardim/irrigacao/{zona_id}/comando`
- payload: `{"acao": "desligar", "origem": "manual"}`
