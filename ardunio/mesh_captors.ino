int ADDR = 0xBE;

int NB_PINS = 4;
boolean started = false;

int led = 11;
int button = 10;
int pins[] = {A0, A1, A2, A3};

int last_time[] = {0, 0, 0, 0};
int last_value[] = {0, 0, 0, 0};

void setup() {
   Serial.begin(9600);
   pinMode(led, OUTPUT);
   pinMode(button, INPUT);
}

void sendFrame(int pin, int value) {
   Serial.write(0x7E);
   Serial.write(ADDR);
   Serial.write(pin);
   Serial.write(value);
}

void loop() {
  if(digitalRead(button) == HIGH) {
    started = !started;
    digitalWrite(led, started);
    while(digitalRead(button) != LOW) delay(50); 
  }
  
  for(int i = 0; i < NB_PINS; i++) {
     int value = analogRead(pins[i]);
     value = constrain(map(value, 0, 1023, 0, 255), 0, 255);
     
     int time = millis();
     
     if(value != last_value[i] && time - last_time[i] >= 500) {
        sendFrame(pins[i], value);
        last_value[i] = value;
        last_time[i] = time;
     }
  }
  delay(50);
}