// Upload este programa al Arduino para apagar los outputs

int OUT5 = 5;
int OUT6 = 6;

const byte relayOnState = LOW;
const byte relayOffState = HIGH;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);

    // Set los variables OUT5 y OUT6 que sean OUTPUT
    pinMode(OUT5, OUTPUT);
    pinMode(OUT6, OUTPUT);

    // Escribir (mandar o cortal senal) al ARDUINO
    digitalWrite(OUT5, relayOffState);
    digitalWrite(OUT6, relayOffState);
    delay(500);
    Serial.print("Arduino Outputs Turned Off");
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
