#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <bluefruit.h>

Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

#define BUTTON_A 31
#define BUTTON_B 30
#define BUTTON_C 27

BLEClientService tamaService = BLEClientService(0xFFF0);
BLEClientCharacteristic txService = BLEClientCharacteristic(0xFFF2);
BLEClientCharacteristic rxService = BLEClientCharacteristic(0xFFF1);

void setup() {
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  // Clear the buffer.
  display.clearDisplay();
  display.display();

  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);

  // text display tests
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);

  Bluefruit.begin(0, 1);
  Bluefruit.setName("Tama-Tamper");
  display.print("TamaTamper 8======D");
  display.display();

  // Initialize client
  tamaService.begin();
  txService.begin();
  rxService.begin();
}

void loop() {
  if(!digitalRead(BUTTON_A)) display.print("Kill ");
  if(!digitalRead(BUTTON_B)) display.print("Feed ");
  if(!digitalRead(BUTTON_C)) display.print("Chet ");
  delay(200);
  yield();
  display.display();
}
