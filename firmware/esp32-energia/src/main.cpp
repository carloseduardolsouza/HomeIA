#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <time.h>

#include "config.h"
#include "pzem_reader.h"
#include "status_led.h"

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

struct ReadingBuffer {
  EnergyReading items[50];
  int start = 0;
  int count = 0;

  void push(const EnergyReading& item) {
    int index = (start + count) % 50;
    items[index] = item;
    if (count < 50) {
      count++;
    } else {
      start = (start + 1) % 50;
    }
  }

  bool pop(EnergyReading& out) {
    if (count == 0) {
      return false;
    }
    out = items[start];
    start = (start + 1) % 50;
    count--;
    return true;
  }
};

ReadingBuffer offlineBuffer;
unsigned long lastPublish = 0;
unsigned long wifiBackoffMs = 1000;
unsigned long mqttBackoffMs = 1000;

void connectWifiWithBackoff() {
  while (WiFi.status() != WL_CONNECTED) {
    setLedState(false, true, false, LED_PIN_R, LED_PIN_Y, LED_PIN_G);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(wifiBackoffMs);
    wifiBackoffMs = min(wifiBackoffMs * 2, 30000UL);
  }
  wifiBackoffMs = 1000;
}

void connectMqttWithBackoff() {
  while (!mqttClient.connected()) {
    setLedState(true, false, false, LED_PIN_R, LED_PIN_Y, LED_PIN_G);
    mqttClient.connect(MEDIDOR_ID, MQTT_USER, MQTT_PASSWORD);
    if (!mqttClient.connected()) {
      delay(mqttBackoffMs);
      mqttBackoffMs = min(mqttBackoffMs * 2, 30000UL);
    }
  }
  mqttBackoffMs = 1000;
}

bool publishReading(const EnergyReading& reading) {
  String topic = String("casa/energia/medidor/") + MEDIDOR_ID;
  StaticJsonDocument<384> doc;
  doc["id"] = MEDIDOR_ID;
  doc["local"] = LOCAL_LABEL;
  doc["tensao_v"] = reading.tensao_v;
  doc["corrente_a"] = reading.corrente_a;
  doc["potencia_w"] = reading.potencia_w;
  doc["potencia_va"] = reading.potencia_va;
  doc["fator_potencia"] = reading.fator_potencia;
  doc["frequencia_hz"] = reading.frequencia_hz;
  doc["energia_kwh"] = reading.energia_kwh;
  doc["ts"] = reading.ts;

  char payload[384];
  serializeJson(doc, payload);
  return mqttClient.publish(topic.c_str(), payload);
}

long nowTs() {
  long ts = (long)time(nullptr);
  if (ts <= 0) {
    ts = (long)(millis() / 1000);
  }
  return ts;
}

void flushBuffer() {
  EnergyReading buffered;
  while (mqttClient.connected() && offlineBuffer.pop(buffered)) {
    if (!publishReading(buffered)) {
      offlineBuffer.push(buffered);
      break;
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupStatusLeds(LED_PIN_R, LED_PIN_Y, LED_PIN_G);
  setLedState(false, true, false, LED_PIN_R, LED_PIN_Y, LED_PIN_G);

  connectWifiWithBackoff();
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");

  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  connectMqttWithBackoff();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWifiWithBackoff();
  }

  if (!mqttClient.connected()) {
    connectMqttWithBackoff();
  }

  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;

    EnergyReading reading = readPzemSensor(nowTs());
    if (!publishReading(reading)) {
      offlineBuffer.push(reading);
    }
    flushBuffer();
  }

  if (WiFi.status() == WL_CONNECTED && mqttClient.connected()) {
    setLedState(false, false, true, LED_PIN_R, LED_PIN_Y, LED_PIN_G);
  }
}
