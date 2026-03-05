# ESP32 Energia (PZEM-004T)

Firmware para coleta de energia e envio MQTT a cada 5 segundos.

## Topico publicado

- `casa/energia/medidor/{id_medidor}`

## Payload

```json
{
  "id": "medidor_01",
  "tensao_v": 220.3,
  "corrente_a": 5.61,
  "potencia_w": 1234.5,
  "potencia_va": 1240.0,
  "fator_potencia": 0.995,
  "frequencia_hz": 60.0,
  "energia_kwh": 542.3,
  "ts": 1709123456
}
```

## Funcionalidades obrigatorias implementadas

- Reconexao automatica WiFi e MQTT com backoff exponencial.
- Buffer local em RAM de 50 leituras quando MQTT indisponivel.
- LED de status:
  - verde = OK (WiFi + MQTT)
  - amarelo = sem WiFi
  - vermelho = sem MQTT

## Pinagem sugerida

```text
ESP32         PZEM-004T
3V3/GND    -> Alimentacao modulo UART isolado
GPIO16 TX  -> RX do modulo
GPIO17 RX  -> TX do modulo
```

## Flash

1. Ajuste `include/config.h`.
2. Rode `pio run -t upload`.
3. Monitore via `pio device monitor`.
