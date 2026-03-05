# Topicos MQTT - HomeIA

| Topico                              | Payload exemplo                                                                                                                                                                                      | Frequencia |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `casa/energia/consumo`              | `{ "watts": 1240.5, "volts": 220.1, "amperes": 5.64, "ts": 1709123456 }`                                                                                                                             | 5s         |
| `casa/energia/disjuntor`            | `{ "id": "disjuntor_01", "status": "closed", "ts": 1709123456 }`                                                                                                                                     | 5s         |
| `casa/energia/medidor/{id_medidor}` | `{ "id": "medidor_01", "tensao_v": 220.3, "corrente_a": 5.61, "potencia_w": 1234.5, "potencia_va": 1240.0, "fator_potencia": 0.995, "frequencia_hz": 60.0, "energia_kwh": 542.3, "ts": 1709123456 }` | 5s         |
| `jardim/solo/umidade`               | `{ "sensor_id": "solo_01", "umidade_pct": 34.2, "ts": 1709123456 }`                                                                                                                                  | 5s         |
| `jardim/solo/temperatura`           | `{ "sensor_id": "solo_01", "temp_c": 22.4, "ts": 1709123456 }`                                                                                                                                       | 5s         |
| `casa/ambiente/temperatura`         | `{ "sensor_id": "amb_01", "temp_c": 24.1, "umidade_pct": 65.0, "ts": 1709123456 }`                                                                                                                   | 5s         |

## Regras de validacao no gateway

- Janela de timestamp: +/- 60 segundos.
- Faixas fisicas:
  - `umidade_pct`: 0..100
  - `temp_c`: -40..85
  - `volts`: 0..300
  - `amperes`: 0..250
  - `watts`: 0..50000
  - `tensao_v`: 0..300
  - `corrente_a`: 0..250
  - `potencia_w`: 0..50000
  - `potencia_va`: 0..50000
  - `fator_potencia`: 0..1
  - `frequencia_hz`: 45..75
  - `energia_kwh`: >= 0
