# Modulo M-03 - Irrigacao

## Fluxo de decisao

1. Leitura de umidade por zona.
2. Consulta de previsao de chuva (OpenWeatherMap) com cache Redis por 30 min.
3. Regras RN-10..RN-13 aplicadas pelo `DecisionEngine`.
4. Se permitido, publicacao de comando MQTT para acionar valvula.

## Regras de negocio implementadas

- RN-10: bloquear se chuva prevista > 5mm.
- RN-11: permitir apenas entre 05h-09h e 18h-21h.
- RN-12: duracao maxima de 60 min.
- RN-13: intervalo minimo de 4h entre sessoes.

## Calibracao do sensor capacitivo

1. Ler valor em solo seco (referencia alta).
2. Ler valor em solo molhado (referencia baixa).
3. Ajustar formula para mapear leitura analogica para `%` entre 0 e 100.
4. Revisar mensalmente por variacao de temperatura e salinidade do solo.

## Arquivos chave

- `services/irrigation-service/src/rules/business_rules.py`
- `services/irrigation-service/src/decision_engine.py`
- `services/irrigation-service/src/weather_client.py`
