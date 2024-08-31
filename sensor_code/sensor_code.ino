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

// Definicija pinova i konstanti za anemometar
int sensorPin = A0;
int sensorValue = 0;
float sensorVoltage = 0;
float windSpeed = 0;
float voltageConversionConstant = 0.004882814;
int sensorDelay = 1000; // 1 sekunda delay za anemometar
float voltageMin = 0.4;
float windSpeedMin = 0;
float voltageMax = 2.0;
float windSpeedMax = 32;

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22, BMP280 & Anemometar - senzori za temperaturu, tlak, vlažnost i brzinu vjetra."));

  // Start DHT senzor
  dht.begin();

  // Start BMP280 senzor
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

  // Provjera jesu li čitanja uspješna za DHT22
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Greška pri čitanju s DHT senzora!"));
  } else {
    Serial.print(F("Vlažnost: "));
    Serial.print(h);
    Serial.print(F("%  Temperatura: "));
    Serial.print(t);
    Serial.println(F("°C"));
  }

  // Ispis tlaka
  Serial.print(F("Tlak: "));
  Serial.print(pressure);
  Serial.println(F(" hPa"));

  // Očitavanje anemometra
  sensorValue = analogRead(sensorPin);
  sensorVoltage = sensorValue * voltageConversionConstant;

  if (sensorVoltage <= voltageMin) {
    windSpeed = 0;
  } else {
    windSpeed = (sensorVoltage - voltageMin) * windSpeedMax / (voltageMax - voltageMin);
  }

  Serial.print("Napon: ");
  Serial.print(sensorVoltage);
  Serial.print(" V\tBrzina vjetra: ");
  Serial.print(windSpeed);
  Serial.println(" m/s");

  delay(3000); // Čekanje tri sekunde prije sljedećeg čitanja
}
