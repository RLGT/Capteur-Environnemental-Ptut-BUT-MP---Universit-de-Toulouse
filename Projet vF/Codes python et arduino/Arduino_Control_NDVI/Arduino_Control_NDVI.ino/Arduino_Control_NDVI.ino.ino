/*****************************************************
 * BIBLIOTHEQUES
 *****************************************************/
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <RTClib.h>
#include <AS726X.h>
#include <Adafruit_BMP280.h>

/*****************************************************
 * CONSTANTES
 *****************************************************/
const int chipSelect = 10;
const uint8_t TCA_ADDR = 0x70;

/*****************************************************
 * INSTANCES
 *****************************************************/
AS726X sensor1;
AS726X sensor2;
Adafruit_BMP280 bme;
RTC_DS1307 rtc;

char dateBuffer[11];
char timeBuffer[9];

/*****************************************************
 * SELECTION CANAL MULTIPLEXEUR
 *****************************************************/

void tcaSelect(uint8_t channel)
{
  if (channel > 7) return;

  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

/*****************************************************
 * SETUP
 *****************************************************/
void setup()
{
  Serial.begin(115200);
  while(!Serial);

  Wire.begin();

  Serial.println("Initialisation...");

  /******** AS726X #1 ********/
  tcaSelect(0);

  if (!sensor1.begin())
  {
    Serial.println("Erreur AS726X #1");
    while(1);
  }

  /******** AS726X #2 ********/
  tcaSelect(2);

  if (!sensor2.begin())
  {
    Serial.println("Erreur AS726X #2");
    while(1);
  }

  /******** BME280 ********/
  tcaSelect(3);
  delay(50);
  if (!bme.begin(0x76))
  {
    Serial.println("Erreur BME280");
    while(1);
  }

  /******** RTC ********/
  tcaSelect(4);

  if (!rtc.begin())
  {
    Serial.println("RTC non detectee");
    while(1);
  }

  if (!rtc.isrunning())
  {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  /******** SD ********/
  if (!SD.begin(chipSelect))
  {
    Serial.println("Erreur carte SD");
    while(1);
  }

  if (!SD.exists("Mesures.csv"))
  {
    File dataFile = SD.open("Mesures.csv", FILE_WRITE);

    if (dataFile)
    {
      dataFile.println("Date;Heure;R1;S1;T1;U1;V1;W1;R2;S2;T2;U2;V2;W2;TempAS1;TempAS2;TempBME;HumBME;PressBME;NDVI");
      dataFile.close();
    }
  }

  Serial.println("Setup terminé");
}

/*****************************************************
 * LOOP
 *****************************************************/
void loop()
{

  /******** RTC ********/
  tcaSelect(4);

  DateTime now = rtc.now();

  sprintf(dateBuffer,"%04d-%02d-%02d",now.year(),now.month(),now.day());
  sprintf(timeBuffer,"%02d:%02d:%02d",now.hour(),now.minute(),now.second());

  /******** AS726X #1 ********/
  tcaSelect(0);

  sensor1.takeMeasurements();

  float R1 = sensor1.getCalibratedR();
  float S1 = sensor1.getCalibratedS();
  float T1 = sensor1.getCalibratedT();
  float U1 = sensor1.getCalibratedU();
  float V1 = sensor1.getCalibratedV();
  float W1 = sensor1.getCalibratedW();
  float tempAS1 = sensor1.getTemperature();

  /******** AS726X #2 ********/
  tcaSelect(2);

  sensor2.takeMeasurements();

  float R2 = sensor2.getCalibratedR();
  float S2 = sensor2.getCalibratedS();
  float T2 = sensor2.getCalibratedT();
  float U2 = sensor2.getCalibratedU();
  float V2 = sensor2.getCalibratedV();
  float W2 = sensor2.getCalibratedW();
  float tempAS2 = sensor2.getTemperature();

  /******** BME280 ********/
  tcaSelect(3);

  float tempBME = bme.readTemperature();
  float pressBME = bme.readPressure() / 100.0;

  /******** NDVI ********/
  float NDVI = 0;

  if ((V1/V2 + S1/S2) != 0 && V2 != 0 && S2 != 0)
  {
    NDVI = ((V1/V2) - (S1/S2)) / ((V1/V2) + (S1/S2));
  }

  /******** SD ********/
  File dataFile = SD.open("Mesures.csv", FILE_WRITE);

  if (dataFile)
  {
    dataFile.print(dateBuffer); dataFile.print(';');
    dataFile.print(timeBuffer); dataFile.print(';');

    dataFile.print(R1); dataFile.print(';');
    dataFile.print(S1); dataFile.print(';');
    dataFile.print(T1); dataFile.print(';');
    dataFile.print(U1); dataFile.print(';');
    dataFile.print(V1); dataFile.print(';');
    dataFile.print(W1); dataFile.print(';');

    dataFile.print(R2); dataFile.print(';');
    dataFile.print(S2); dataFile.print(';');
    dataFile.print(T2); dataFile.print(';');
    dataFile.print(U2); dataFile.print(';');
    dataFile.print(V2); dataFile.print(';');
    dataFile.print(W2); dataFile.print(';');

    dataFile.print(tempAS1); dataFile.print(';');
    dataFile.print(tempAS2); dataFile.print(';');

    dataFile.print(tempBME); dataFile.print(';');
    dataFile.print(pressBME); dataFile.print(';');

    dataFile.println(NDVI);

    dataFile.close();
  }

  /******** SERIAL ********/
  Serial.print(dateBuffer);
  Serial.print(" ");
  Serial.println(timeBuffer);

  Serial.print("NDVI: ");
  Serial.println(NDVI);

    Serial.print(tempBME);  Serial.print("°C"); Serial.print(" "); Serial.print(';');
    Serial.print(pressBME); Serial.println("hPa"); 

  Serial.println("----------------");

  delay(2000);
}