# Modulo M-01 - Modelos Preditivos e Alertas

## Modelos

- Isolation Forest:
  - Execucao: job periodico (ex.: a cada 5 min).
  - Detecta pontos anomalos de consumo em relacao ao comportamento historico.
- Modelo de Forecast (Prophet wrapper):
  - Execucao: job horario/diario para prever proximas 24h.
  - Detecta tendencia de consumo e sazonalidade.
- Billing Estimator:
  - Execucao: junto ao forecast.
  - Projeta fatura mensal com base no consumo acumulado e tarifa.

## Metricas de treino (referencia inicial)

- Anomaly precision: 0.92
- Anomaly recall: 0.87
- Forecast MAE: 118.4
- Forecast MAPE: 14.7%

## Como retreinar manualmente

1. Subir infraestrutura da Entrega 02.
2. Executar notebooks em `notebooks/treinamento/` na ordem:
   - `energia-eda.ipynb`
   - `energia-baseline.ipynb`
   - `energia-isolation-forest.ipynb`
   - `energia-prophet.ipynb`
3. Validar metricas alvo.
4. Rodar `python -m src.main` em `services/inference-engine`.

## Como interpretar alertas

- `CRITICO`: score de anomalia abaixo do threshold configurado.
- `AVISO`: pico acima do percentual da media esperada na janela.
- Cooldown de 15 minutos evita spam de notificacoes consecutivas.

## Pipeline

Dados (InfluxDB) -> Preprocessamento -> Modelo (Isolation/Forecast) -> Decisao -> Alerta (Telegram)
