#pragma once

#include <PubSubClient.h>
#include <WiFi.h>

inline void connectWifi(const char* ssid, const char* password) {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

inline void ensureMqttConnected(PubSubClient& client, const char* deviceId, const char* user, const char* pass) {
  while (!client.connected()) {
    client.connect(deviceId, user, pass);
    if (!client.connected()) {
      delay(2000);
    }
  }
}
