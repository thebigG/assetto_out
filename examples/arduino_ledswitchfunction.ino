#include <ArduinoJson.h>

int LED = 13;
void helloworld() {
  Serial.println("hello world");
}
void ledswitch(float break_pressure) {

if (break_pressure>=0.3) {
  int LED = (13);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

}
else {
  pinMode(LED,OUTPUT);
  digitalWrite(LED,LOW);



}



}



int break_pressure = 1;
void setup() {
  // put your setup code here, to run once:
  //helloworld()
  Serial.begin(9600);
  Serial.setTimeout(100);
}

void loop() {
while (Serial.available() == 0) {}     //wait for data available
  
String brakevalue = Serial.readStringUntil('\r');
brakevalue.trim();

const char* input = "{\"brake\":\"0\"}";
StaticJsonDocument<256> doc;

DeserializationError err = deserializeJson(doc, brakevalue);

if(err) {
  //Serial.print("ERROR: ");
  //Serial.println(err.c_str());
  return;
}


const char* brake = doc["brake"];
Serial.println(brake);
  
String brake_str{brake};
  
  
  ledswitch(brake_str.toFloat());
 
}
