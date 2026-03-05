#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "config.h"
#include "mqtt_client.h"
#include "sensors.h"

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

unsigned long lastPublish = 0;

void publishEnergy(long ts) {
  EnergyData energy = readEnergy();
  StaticJsonDocument<256> doc;
  doc["watts"] = energy.watts;
  doc["volts"] = energy.volts;
  doc["amperes"] = energy.amperes;
  doc["ts"] = ts;
  char payload[256];
  serializeJson(doc, payload);
  mqttClient.publish("casa/energia/consumo", payload);
}

void publishBreaker(long ts) {
  StaticJsonDocument<128> doc;
  doc["id"] = "disjuntor_01";
  doc["status"] = "closed";
  doc["ts"] = ts;
  char payload[128];
  serializeJson(doc, payload);
  mqttClient.publish("casa/energia/disjuntor", payload);
}

void publishSoil(long ts) {
  SoilData soil = readSoil();
  StaticJsonDocument<192> docUmidade;
  docUmidade["sensor_id"] = "solo_01";
  docUmidade["umidade_pct"] = soil.umidade_pct;
  docUmidade["ts"] = ts;
  char payloadUmidade[192];
  serializeJson(docUmidade, payloadUmidade);
  mqttClient.publish("jardim/solo/umidade", payloadUmidade);

  StaticJsonDocument<192> docTemp;
  docTemp["sensor_id"] = "solo_01";
  docTemp["temp_c"] = soil.temp_c;
  docTemp["ts"] = ts;
  char payloadTemp[192];
  serializeJson(docTemp, payloadTemp);
  mqttClient.publish("jardim/solo/temperatura", payloadTemp);
}

void publishAmbient(long ts) {
  AmbientData ambient = readAmbient();
  StaticJsonDocument<192> doc;
  doc["sensor_id"] = "amb_01";
  doc["temp_c"] = ambient.temp_c;
  doc["umidade_pct"] = ambient.umidade_pct;
  doc["ts"] = ts;
  char payload[192];
  serializeJson(doc, payload);
  mqttClient.publish("casa/ambiente/temperatura", payload);
}

void setup() {
  Serial.begin(115200);
  connectWifi(WIFI_SSID, WIFI_PASSWORD);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
}

void loop() {
  ensureMqttConnected(mqttClient, DEVICE_ID, MQTT_USER, MQTT_PASSWORD);
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;
    long ts = (long)(time(nullptr));
    if (ts <= 0) {
      ts = now / 1000;
    }
    publishEnergy(ts);
    publishBreaker(ts);
    publishSoil(ts);
    publishAmbient(ts);
  }
}
