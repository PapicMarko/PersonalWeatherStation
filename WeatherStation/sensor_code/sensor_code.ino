#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>

// Definicija pinova za DHT22
#define DHTPIN 2     // Digitalni pin na kojem je povezan DHT22
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

// Kreiranje instance za BMP280
Adafruit_BMP280 bmp; // I2C

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22 & BMP280 senzori za temperaturu i tlak."));

  // Start DHT sensor
  dht.begin();

  // Start BMP280 sensor
  if (!bmp.begin(0x77)) {   // Promijeni na 0x77 ako je adresa BMP280 senzora 0x77
    Serial.println(F("Nije moguće pronaći BMP280 senzor!"));
    while (1);
  }
}

void loop() {
  // Čitanje vlažnosti i temperature s DHT22
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Čitanje temperature i tlaka s BMP280
  float pressure = bmp.readPressure() / 100.0; // Konverzija u hPa

  // Provjera jesu li čitanja uspješna
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Greška pri čitanju s DHT senzora!"));
  } else {
    Serial.print(F("Vlažnost: "));
    Serial.print(h);
    Serial.print(F("%  Temperatura: "));
    Serial.print(t);
    Serial.println(F("°C"));
  }

  Serial.print(F("Tlak: "));
  Serial.print(pressure);
  Serial.println(F(" hPa"));

  delay(10000); // Čekanje dvije sekunde prije sljedećeg čitanja
}
