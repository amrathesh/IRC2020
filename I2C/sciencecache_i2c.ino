#include<Stepper.h>
#include <dht.h>
#include <SHT1x.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP280.h"
#include "MQ7.h"
//Initialise variable for Colour Sensor
int frequency=0;

#define address 0x6
//Defining Colour Sensor Inputs
#define CS0 31 //Yellow J-Brown
#define CS1 33 //Green  J-Yellow
#define CS2 35 //Grey   J-Red
#define CS3 37 //Purple J-Orange
#define CSLED 39 //Orange J-white
#define CSOut 41 //White  J-Green
#define CSRED 43 //       J-black

//Defining Enables For Linear Actuator and Auger
#define LA_AG_EN 14

//Defining Enables For Water Pump and Transer Pump
#define WP_TP_EN 15

//Defining Enables for Test Tube Pump
#define TTP_EN  16

//Defining pins,delay for Linear Actuator
#define LAL 22
#define LAR 24
#define LAD 1500

//Defining pins,delay for Auger
#define AGML 26
#define AGMR 28
#define AGD 2000

//Define pins,delay for Water Pump
#define WPML 30
#define WPMR 32
#define WPD 5000

//Define pins,delay for Transfer Pump
#define TPML 34
#define TPMR 36
#define TPMD 32000

//Define pins,delay for Test Tube Pump
#define TTPML 40
#define TTPMR 42
#define TTPD 3800
#define TTIP 11000

//Define pins for Auger Stepper
#define ASSPR 1000
#define AGS0 6 
#define AGS1 7 
#define AGS2 8
#define AGS3 9
#define ASSPD 10
#define ASSTP 40
#define ASDEL 1000

//Define pins for Test Tube Stepper
#define TTSPR 200
#define TTS0  10
#define TTS1  11
#define TTS2  12
#define TTS3  13
#define TTSSPD 40
#define TTSTP 17
#define TTDSTP 34
#define TTDEL 500

//Setting up the Auger Stepper and Test Tube Stepper
Stepper AugerStepper(ASSPR, AGS0,AGS1,AGS2,AGS3);
Stepper TestTubeStepper(TTSPR,TTS0,TTS1,TTS2,TTS3);

//Defining SHT-10 Sensor Inputs
#define dataPin  4
#define clockPin 5
SHT1x sht1x(dataPin, clockPin);
float temp_c;
float humidity;
//Red = VCC (3-5VDC)
//Black or Green = Ground
//Yellow = Clock
//Blue = Data
//connect a 10K resistor from the blue Data line to VCC
//y-11-clk   b-10   g-gnd   red-vcc

//definition for BMP280_sensor
Adafruit_BMP280 bmp; // I2C
float pressure;    //To store the barometric pressure (Pa)  
int altimeter;    //To store the altimeter (m) (you can also use it as a float variable)
   
//Defining DHT-11 Sensor Inputs
#define dht_apin A0 //put DHT11 to A0 only
dht DHT;

//definition for MQ4
#define MQ4_sensorpin A1 //Sensor pin
float m = -0.318; //Slope
float b = 1.133; //Y-Intercept
float R0 = 1.85;
float MQ4ppm;

//definition for MQ7
#define MQ7_sensorpin A2

MQ7 mq7(A2,5.0);
float MQ7ppm;
int count=0;

//definition for MQ135
#define MQ135_sensorpin A3
float MQ135ppm;  


int data[14];
int n=14;

//Ultra_Sound sensor declarations
#define trigpin 50
#define echopin 52
long duration;
int distance;

void setup() {
 //Setting up pins for Colour Sensor
  Wire.begin(address); // Start I2C Bus as slave
  Wire.onRequest(myWrite);
  pinMode(CS0, OUTPUT);
  pinMode(CS1, OUTPUT);
  pinMode(CS2, OUTPUT);
  pinMode(CS3, OUTPUT);
  pinMode(CSLED,OUTPUT);
  pinMode(CSOut, INPUT);
  pinMode(CSRED,OUTPUT);

 //Setting frequency-scaling to 20% for Colour Sensor
 digitalWrite(CS0,HIGH);
 digitalWrite(CS1,LOW);
 digitalWrite(CSRED,HIGH);
 digitalWrite(CSLED,LOW);

 //Setting up pins for Enabling Auger Motor and Linear Actuator
 pinMode(LA_AG_EN,OUTPUT);

 //Setting up pins for Enabling Water Pump and Transfer Pump
 pinMode(WP_TP_EN,OUTPUT);

 //Setting up pins for Enabling Test Tube Pump
 pinMode(TTP_EN,OUTPUT);
 
 
 //Setting up pins for Linear Actuator
 pinMode(LAL,OUTPUT);
 pinMode(LAR,OUTPUT);

 //Setting up pins for Auger
 pinMode(AGML,OUTPUT);
 pinMode(AGMR,OUTPUT);

 //Setting up pins for Water Pump
 pinMode(WPML,OUTPUT);
 pinMode(WPMR,OUTPUT);

 //Setting up pins for Transfer Pump
 pinMode(TPML,OUTPUT);
 pinMode(TPMR,OUTPUT);

 //Setting up pins for Test Tube Pump
 pinMode(TTPML,OUTPUT);
 pinMode(TTPMR,OUTPUT);

 //Setting up Speed for Steppers
 AugerStepper.setSpeed(ASSTP);
 TestTubeStepper.setSpeed(TTSSPD);

//BMP280 setup
bmp.begin(0x76);    //Begin the sensor  

//ultra_sound setup
pinMode(trigpin,OUTPUT);//ultra_sound
pinMode(echopin,INPUT);//ultra_sound

Serial.begin(9600);
}
//---------------------------------------------------------------------------END OF SETUP-----------------------------------------------------------//
void ObtainSoil()
{
 //Enable  LA and AG
 digitalWrite(LA_AG_EN,HIGH);  
 
 //Lower LA
 digitalWrite(LAL,HIGH);
 digitalWrite(LAR,LOW);
 delay(LAD);

 //Stop LA
 digitalWrite(LAL,LOW);
 digitalWrite(LAR,LOW);
 
 
 //Start Drilling
 digitalWrite(AGML,LOW);
 digitalWrite(AGMR,HIGH);
 delay(AGD);
 Serial.println("Stop Drilling");

 //Stop Drilling
 digitalWrite(AGML,LOW);
 digitalWrite(AGMR,LOW);

 //Raise LA
 digitalWrite(LAL,LOW);
 digitalWrite(LAR,HIGH);
 delay(LAD);

  //Stop LA
 digitalWrite(LAL,LOW);
 digitalWrite(LAR,LOW);


 //Rotate Stepper
 AugerStepper.step(ASSTP);
 delay(ASDEL);

 //Reverse Drilling 
 digitalWrite(AGML,HIGH);
 digitalWrite(AGMR,LOW);
 delay(AGD);

 //Stop Drilling
 digitalWrite(AGML,LOW);
 digitalWrite(AGMR,LOW);
 delay(AGD);

 //Disable LA and AG
 digitalWrite(LA_AG_EN,LOW);
 Serial.println("Soil Obtained");
 
}
void PrepareSolution()
{
  //Enable Water Pump and Transfer Pump 
  digitalWrite(WP_TP_EN,HIGH);

  //Start Water Pump
  digitalWrite(WPML,HIGH);
  digitalWrite(WPMR,LOW);
  delay(WPD);

  //Stop Water Pump
  digitalWrite(WPML,LOW);
  digitalWrite(WPMR,LOW);
  
  //Start Transfer Pump
  digitalWrite(TPML,LOW);
  digitalWrite(TPMR,HIGH);
  delay(TPMD);

  //Stop Transfer Pump
  digitalWrite(TPML,LOW);
  digitalWrite(TPMR,LOW);
  
  //Disable Water Pump and Transfer Pump 
  digitalWrite(WP_TP_EN,LOW); 

   Serial.println("Solution Prepared");
}

void FillTestTube()
{
  
  //Enable Test Tube Pump
  digitalWrite(TTP_EN,HIGH);

  int rotation=0;

 
  digitalWrite(TTPML,HIGH);
  digitalWrite(TTPMR,LOW);
  delay(TTIP);
  
  digitalWrite(TTPML,LOW);
  digitalWrite(TTPMR,LOW);
  delay(TTIP);

  
  
  for(rotation=1;rotation<=4;rotation+=1)
  {
   
  digitalWrite(TTPML,HIGH);
  digitalWrite(TTPMR,LOW);
  delay(TTPD);
  
  digitalWrite(TTPML,LOW);
  digitalWrite(TTPMR,LOW);
  delay(TTPD);
  
  Serial.print("Rotation ");
  Serial.println(rotation);
  
  
  if(rotation%2==0)
  {
    
  TestTubeStepper.step(TTDSTP);
  delay(TTDEL);
    
  }
  
  else{
  TestTubeStepper.step(TTSTP);
  delay(TTDEL);
  }
  
  
  }  
  
  //Disable Test Tube Pump   
  digitalWrite(TTP_EN,LOW);
  Serial.println("Filling Done");
  
}
void NPKTest()
{

  digitalWrite(CS2,LOW);
  digitalWrite(CS3,LOW);
  digitalWrite(CSLED,LOW);
  digitalWrite(CSRED,LOW);

  
  
  int rotation=0;
   for(rotation=1;rotation<=4;rotation+=1)
  {
   
  Serial.print("Rotation ");
  Serial.println(rotation);
  
  frequency = pulseIn(CSOut, LOW);
  // Printing the value on the serial monitor
  Serial.print("Reading 1= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.println("  ");
  delay(100);
  
  frequency = pulseIn(CSOut, LOW);
  // Printing the value on the serial monitor
  Serial.print("Reading 2= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.println("  ");
  delay(100);
  
  frequency = pulseIn(CSOut, LOW);
  // Printing the value on the serial monitor
  Serial.print("Reading 3= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.println("  ");
  delay(100);

  if(rotation%2==0)
  {
    
  TestTubeStepper.step(TTDSTP);
  delay(TTDEL);
    
  }
  else{
  TestTubeStepper.step(TTSTP);
  delay(TTDEL);
  }
  
  
  }  
}
   
//Fuction for SHT-10
void Sht_sensor()
{
  temp_c = sht1x.readTemperatureC();
  humidity = sht1x.readHumidity();

  // Print the values to the serial port
  Serial.print("Soil Temperature: ");
  Serial.print(temp_c, DEC);
  Serial.print("C ");
  Serial.print("Soil Humidity: ");
  Serial.print(humidity);
  Serial.println("%");
}
   
//function for MQ4 sensor
void MQ4_sensor()
{
  float sensor_volt=0; //Define variable for sensor voltage
  float RS_gas=0; //Define variable for sensor resistance
  float ratio=0; //Define variable for ratio
  float sensorValue = analogRead(MQ4_sensorpin); //Read analog values of sensor
  sensor_volt = sensorValue * (5.0 / 1023.0); //Convert analog values to voltage
  RS_gas = ((5.0 * 1.0) / sensor_volt) - 1.0; //Get value of RS in a gas
  ratio = RS_gas / R0;   // Get ratio RS_gas/RS_air
  MQ4ppm = (log10(ratio) - b) / m; //Get ppm value in linear scale according to the the ratio value
  Serial.print("MQ4 READING: ");
  Serial.print(MQ4ppm);
  Serial.println("\t");
}

//function for MQ7 sensor
void MQ7_sensor()
{
    Serial.print("MQ7 READING: ");
    MQ7ppm=mq7.getPPM();
    Serial.print(MQ7ppm);
    Serial.println("\t");
}

//function for MQ135 sensor
void MQ135_sensor()
{
  MQ135ppm = analogRead(MQ135_sensorpin); // read analog input pin 0
  Serial.print("MQ135 reading: ");
  MQ135ppm=MQ135ppm+285;
  Serial.println(MQ135ppm);
  delay(1000); // wait 2s for next reading
}
//Function for DHT-11
void Dht_sensor()
{
    DHT.read11(dht_apin);
    Serial.print("Current atmosphere humidity = ");
    Serial.print(DHT.humidity);
    Serial.print("%  ");
    Serial.print("atmosphere temperature = ");
    Serial.print(DHT.temperature); 
    Serial.println("C  ");
    delay(5000);//Wait 5 seconds before accessing sensor again.
}
//Function for BMP-280 sensor
void BMP280_sensor()
{
   pressure = bmp.readPressure()*0.9869/100000;
   altimeter = bmp.readAltitude (1050.35); //Change the "1050.35" to your city current barrometric pressure (https://www.wunderground.com)
    Serial.print("Pressure: ");
    Serial.print(pressure);
    Serial.print(" atm");
    Serial.print("\t");
    Serial.print("Elevation: ");
    Serial.print(altimeter); // this should be adjusted to your local forcase
    Serial.println(" m");
    delay(500); //Update every 5 sec
}

void myWrite()
{
  static int i=0;
  Wire.write(data[i]); // sends a[i]
  i++;
  if(i>=n)
    i=0;
}
  

void  loop()
{
  
  char ch;
/*  if(Serial.available()>0)
  {
  ch=Serial.read();
  
  }*/
  //Serial.println("hmvnm");
  Dht_sensor();
  MQ4_sensor();
  MQ7_sensor();
  MQ135_sensor();
  BMP280_sensor();
/* digitalWrite(LA_AG_EN,HIGH);  
 //Lower LA
 digitalWrite(LAL,LOW);
 digitalWrite(LAR,HIGH);
 delay(LAD);
 digitalWrite(LAL,LOW);
 digitalWrite(LAR,LOW);
 delay(LAD);

*//*
  Sht_sensor();
  MQ4_sensor();
  MQ7_sensor();
  MQ135_sensor();
  Dht_sensor();
  BMP280_sensor();
  data[0]= 123;
  data[1]=MQ4ppm*100;
  data[2]=MQ7ppm;
  data[3]=MQ135ppm/2;
  data[4]=DHT.humidity;
  data[5]=DHT.temperature;
  data[6]=pressure*100;
  data[7]=temp_c;
  data[8]=humidity;
  data[9]=altimeter*10;
  data[10]=0;
  data[11]=1;
  data[12]=0;
  data[13]=1;  // 0 andre low 1 andre high 
  delay(500);
 //ultrasonic();
// digitalWrite(LA_AG_EN,HIGH);  
 //Start Drilling

// delay(AGD);
digitalWrite(LAL,LOW );
digitalWrite(LAR,HIGH);
*/
}
