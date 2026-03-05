#pragma once

#include <Arduino.h>

inline void setupStatusLeds(int redPin, int yellowPin, int greenPin) {
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
}

inline void setLedState(bool red, bool yellow, bool green, int redPin, int yellowPin, int greenPin) {
  digitalWrite(redPin, red ? HIGH : LOW);
  digitalWrite(yellowPin, yellow ? HIGH : LOW);
  digitalWrite(greenPin, green ? HIGH : LOW);
}
