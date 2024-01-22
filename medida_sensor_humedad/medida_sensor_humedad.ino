int OUT1 = 2;
int Pin1 = A0; 
float value1 = 0;

const byte relayOnState = LOW;
const byte relayOffState = HIGH;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(OUT1, OUTPUT);
  pinMode(Pin1, INPUT);
  
  digitalWrite(OUT1, relayOffState);
  delay(500);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("MOISTURE LEVEL:");
  value1 = analogRead(Pin1);
  Serial.println(value1);
//  if(value1>550)
//  {
//    digitalWrite(OUT1, relayOffState);
//  }
//  else
//  {
//    digitalWrite(OUT1, relayOnState);
//    delay(100);
//    digitalWrite(OUT1, relayOffState);
//  }
    Serial.println();
  delay(1000);
}
