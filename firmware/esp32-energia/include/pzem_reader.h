#pragma once

struct EnergyReading {
  float tensao_v;
  float corrente_a;
  float potencia_w;
  float potencia_va;
  float fator_potencia;
  float frequencia_hz;
  float energia_kwh;
  long ts;
};

inline EnergyReading readPzemSensor(long ts) {
  // Placeholder para PZEM-004T; trocar pela leitura real via UART.
  return {220.3f, 5.61f, 1234.5f, 1240.0f, 0.995f, 60.0f, 542.3f, ts};
}
