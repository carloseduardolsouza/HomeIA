# ESP32 Sensores - Firmware de Ingestao

Firmware base para publicar leituras no broker MQTT a cada 5 segundos.

## Estrutura

- `platformio.ini`
- `include/config.h`
- `include/sensors.h`
- `include/mqtt_client.h`
- `src/main.cpp`

## Wiring (exemplo)

```
ESP32  -> Sensor
3V3    -> VCC
GND    -> GND
GPIO34 -> Umidade analogica
GPIO4  -> DHT data
```

## Flash

1. Instale PlatformIO.
2. Configure `include/config.h` com WiFi e MQTT.
3. Rode `pio run -t upload`.
4. Abra serial monitor: `pio device monitor`.

## Topicos publicados

- `casa/energia/consumo`
- `casa/energia/disjuntor`
- `jardim/solo/umidade`
- `jardim/solo/temperatura`
- `casa/ambiente/temperatura`
