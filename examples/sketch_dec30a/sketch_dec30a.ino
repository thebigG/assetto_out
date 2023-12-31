int counter = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.println("Hello from Arduino");
  // Serial.readString();
  while (Serial.available() == 0) {}     //wait for data available
  String teststr = Serial.readString();
  teststr += counter;
  counter++;
  Serial.println(teststr);
  delay(100);
}
