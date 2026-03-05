# ESP32 Irrigacao

Firmware para leitura de umidade/temperatura e controle de rele da valvula via MQTT.

## Topicos publicados

- `jardim/solo/{zona_id}/umidade`
- `jardim/solo/{zona_id}/temperatura`
- `jardim/irrigacao/{zona_id}/status`

## Topico subscrito

- `jardim/irrigacao/{zona_id}/comando`
  - `{"acao":"ligar","duracao_minutos":12,"origem":"ia"}`
  - `{"acao":"desligar","origem":"manual"}`

## Diagrama de ligacao (sensor + rele + valvula)

```text
ESP32         Sensor Umidade / DHT / Rele
3V3        -> VCC sensores
GND        -> GND sensores e modulo rele
GPIO34     -> AOUT umidade capacitivo
GPIO4      -> DHT22 data
GPIO26     -> IN modulo rele (valvula)
```

## Flash

1. Ajuste credenciais em `include/config.h`.
2. Rode `pio run -t upload`.
3. Monitore com `pio device monitor`.
