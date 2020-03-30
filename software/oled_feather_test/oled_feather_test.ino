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
BLEClientCharacteristic txChar = BLEClientCharacteristic(0xFFF2);
BLEClientCharacteristic rxChar = BLEClientCharacteristic(0xFFF1);

const char* handshake = "f08d54414d41474f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020100001700000000007c68489775a64e9900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000104ad05f0cdf08e0d";

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  display.clearDisplay();
  display.display();

  Serial.begin(9600);

  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);

  // text display tests
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);

  Bluefruit.begin(0, 1);
  Bluefruit.setName("Tama-Tamper");
  display.print("ble whore");
  display.display();
  Serial.print("Initalizing...");
  // Initialize client
  tamaService.begin();
  txChar.begin();
  rxChar.setNotifyCallback(rx_notify_callback);
  rxChar.begin();
  Serial.print("Starting Central... ");
  // Callbacks for Central
  Bluefruit.Central.setDisconnectCallback(disconnect_callback);
  Bluefruit.Central.setConnectCallback(connect_callback);

  Bluefruit.Scanner.setRxCallback(scan_callback);
  Bluefruit.Scanner.restartOnDisconnect(true);
  Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  Bluefruit.Scanner.filterRssi(-50);
  Bluefruit.Scanner.useActiveScan(false);
  Bluefruit.Scanner.start(0);                   // // 0 = Don't stop scanning after n seconds
}

void loop() {
  if(!digitalRead(BUTTON_A)) display.print("Kill ");
  if(!digitalRead(BUTTON_B)) display.print("Feed ");
  if(!digitalRead(BUTTON_C)) {display.clearDisplay();display.setCursor(0,0);}
  delay(200);
  yield();
  display.display();
}

void rx_notify_callback(BLEClientCharacteristic* chr, uint8_t* data, uint16_t len)
{
  Serial.print("<------ ");

  if ( data[0] & bit(0) )
  {
    uint16_t value;
    memcpy(&value, data+1, 2);

    Serial.println(value);
  }
  else
  {
    Serial.println(data[1]);
  }
}

/**
 * Callback invoked when scanner pick up an advertising data
 * @param report Structural advertising data
 */
void scan_callback(ble_gap_evt_adv_report_t* report)
{
  Bluefruit.Central.connect(report);
}

/**
 * Callback invoked when an connection is established
 */
void connect_callback(uint16_t conn_handle)
{
  Serial.println("Connected");
  Serial.print("Discovering Tama Service ... ");

  // If not found, disconnect and return
  if ( !tamaService.discover(conn_handle) )
  {
    Serial.println("Found NONE");

    // disconnect since we couldn't find service
    Bluefruit.disconnect(conn_handle);

    return;
  }

  // Once service is found, we continue to discover its characteristic
  Serial.println("Found it");
  
  Serial.print("Discovering RX characteristic ... ");
  if ( !rxChar.discover() )
  {
    // chr is mandatory, if it is not found (valid), then disconnect
    Serial.println("not found !!!");  
    Serial.println("RX is mandatory but not found");
    Bluefruit.disconnect(conn_handle);
    return;
  }
  Serial.println("Found it");

  Serial.print("Discovering TX characteristic ... ");
  if ( !txChar.discover() )
  {
    // chr is mandatory, if it is not found (valid), then disconnect
    Serial.println("not found !!!");  
    Serial.println("TX is mandatory but not found");
    Bluefruit.disconnect(conn_handle);
    return;
  }
  Serial.println("Found it");

  // Reaching here means we are ready to go, let's enable notification on measurement chr
  if ( rxChar.enableNotify() )
  {
    Serial.println("Ready to receive values");

    Serial.println("Shaking hands with this wreched thing... ");
    txChar.write("", 0);
    txChar.write("f08d", 4);
    txChar.write("54414d41474f0000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000201000017000000", 40);
    txChar.write("00007c68489775a64e9900000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("0000000000000000000000000000000000000000", 40);
    txChar.write("00000000000000000000000010000104ad05", 36);
    txChar.write("f0cd", 4);
    txChar.write("f08e0d", 6);
  }else
  {
    Serial.println("Couldn't enable. Increase DEBUG LEVEL for troubleshooting");
  }
}

/**
 * Callback invoked when a connection is dropped
 * @param conn_handle
 * @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
 */
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}
