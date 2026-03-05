# Inference Engine - M01 Energia

Servico de inferencia para:

- deteccao de anomalias de consumo (Isolation Forest)
- previsao de consumo futuro (modelo de forecast)
- projecao de fatura mensal
- envio de alertas Telegram

## Execucao local

1. `python -m venv .venv`
2. `./.venv/Scripts/activate` (Windows)
3. `pip install -r requirements.txt`
4. `python -m src.main`

## Variaveis de ambiente principais

- `INFLUXDB_URL`, `INFLUXDB_TOKEN`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET`
- `MLFLOW_TRACKING_URI`
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- `ALERT_RULES_PATH` (default: `config/alert_rules.yml`)

## Testes

- `pytest --cov=src --cov-report=term-missing`
