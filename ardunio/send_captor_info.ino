int led=11;
int detector = A0;
int linear = A1;
int joystickx = A2;
int joysticky = A3;

int last_values[] = {0,0,0,0};
int last_time[] = {0,0,0,0};
void setup(){
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  delay(1000);
}

void loop(){
  read(detector, 0);
  read(linear, 1);
  read(joystickx, 2);
  read(joysticky, 3);
  delay(50);
}

void writeFrame(int byte3, int byte4) {
  Serial.write(0x7E);
  Serial.write(0xCB);
  Serial.write(byte3);
  Serial.write(byte4);
  
}

void read(int pin, int index) {
  int value = map(analogRead(pin), 0, 1023, 0, 255);
  if(value != last_values[index] && millis() - last_time[index] > 500) {
    last_values[index] = value;
    last_time[index] = millis();
    digitalWrite(led, HIGH);
    writeFrame(pin, value);
    digitalWrite(led, LOW);
  }
}
