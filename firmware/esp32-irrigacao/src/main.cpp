#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "config.h"

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

unsigned long lastPublish = 0;

float fakeSoilMoisturePct() { return 34.2f; }
float fakeTempC() { return 22.4f; }

void onMessage(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  String commandTopic = String("jardim/irrigacao/") + ZONA_ID + "/comando";
  if (String(topic) != commandTopic) {
    return;
  }

  StaticJsonDocument<192> doc;
  DeserializationError err = deserializeJson(doc, msg);
  if (err) {
    return;
  }

  const char* acao = doc["acao"] | "";
  if (String(acao) == "ligar") {
    digitalWrite(RELAY_PIN, HIGH);
  }
  if (String(acao) == "desligar") {
    digitalWrite(RELAY_PIN, LOW);
  }
}

void ensureWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void ensureMqtt() {
  while (!mqttClient.connected()) {
    mqttClient.connect("esp32-irrigacao", MQTT_USER, MQTT_PASSWORD);
    if (!mqttClient.connected()) {
      delay(2000);
    }
  }
  String commandTopic = String("jardim/irrigacao/") + ZONA_ID + "/comando";
  mqttClient.subscribe(commandTopic.c_str());
}

void publishReadings(long ts) {
  String umidadeTopic = String("jardim/solo/") + ZONA_ID + "/umidade";
  String tempTopic = String("jardim/solo/") + ZONA_ID + "/temperatura";
  String statusTopic = String("jardim/irrigacao/") + ZONA_ID + "/status";

  StaticJsonDocument<192> umidade;
  umidade["zona"] = ZONA_ID;
  umidade["umidade_pct"] = fakeSoilMoisturePct();
  umidade["ts"] = ts;
  char umidadePayload[192];
  serializeJson(umidade, umidadePayload);
  mqttClient.publish(umidadeTopic.c_str(), umidadePayload);

  StaticJsonDocument<192> temp;
  temp["zona"] = ZONA_ID;
  temp["temp_c"] = fakeTempC();
  temp["ts"] = ts;
  char tempPayload[192];
  serializeJson(temp, tempPayload);
  mqttClient.publish(tempTopic.c_str(), tempPayload);

  StaticJsonDocument<192> status;
  status["zona"] = ZONA_ID;
  status["ativo"] = digitalRead(RELAY_PIN) == HIGH;
  status["ts"] = ts;
  char statusPayload[192];
  serializeJson(status, statusPayload);
  mqttClient.publish(statusTopic.c_str(), statusPayload);
}

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  Serial.begin(115200);
  ensureWiFi();
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  mqttClient.setCallback(onMessage);
}

void loop() {
  ensureWiFi();
  ensureMqtt();
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;
    long ts = (long)(millis() / 1000);
    publishReadings(ts);
  }
}
