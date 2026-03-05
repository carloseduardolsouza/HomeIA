#pragma once

struct EnergyData {
  float watts;
  float volts;
  float amperes;
};

struct SoilData {
  float umidade_pct;
  float temp_c;
};

struct AmbientData {
  float temp_c;
  float umidade_pct;
};

inline EnergyData readEnergy() {
  return {1240.5f, 220.1f, 5.64f};
}

inline SoilData readSoil() {
  return {34.2f, 22.4f};
}

inline AmbientData readAmbient() {
  return {24.1f, 65.0f};
}
