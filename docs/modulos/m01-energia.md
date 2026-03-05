# Modulo M-01 - Energia

## Objetivo

Coletar e armazenar dados eletricos do medidor PZEM-004T via ESP32 com envio MQTT em janela de 5 segundos.

## Topico MQTT

- `casa/energia/medidor/{id_medidor}`

## Schema InfluxDB

Measurement: `energia_consumo`

Tags:

- `medidor_id` (string)
- `local` (string, por exemplo `sala`, `cozinha`)

Fields:

- `tensao_v` (float)
- `corrente_a` (float)
- `potencia_w` (float)
- `potencia_va` (float)
- `fator_potencia` (float)
- `frequencia_hz` (float)
- `energia_kwh` (float)

Timestamp:

- unix seconds no payload
- persistido como timestamp temporal no InfluxDB

## Frequencia de coleta

- Publicacao a cada 5 segundos.

## Limites fisicos esperados

- `tensao_v`: 0..300
- `corrente_a`: 0..250
- `potencia_w`: 0..50000
- `potencia_va`: 0..50000
- `fator_potencia`: 0..1
- `frequencia_hz`: 45..75
- `energia_kwh`: >= 0

## Dashboard

Arquivo: `infra/configs/grafana/dashboards/energia-tempo-real.json`
Painel inclui potencia atual, historico 24h, consumo diario, custo estimado, consumo horario e tabela de leituras brutas.
