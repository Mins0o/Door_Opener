#include <Wire.h>
int prev = 500;
int pres;
byte oneByte;
int soundRead;

void setup(){
  Serial.begin(9600);
}

void loop(){
  soundRead=analogRead(A3);
  pres=prev*0.6+soundRead*0.4;
  oneByte=(byte)(pres/4);
  Serial.write(oneByte);
  delay(9);
  prev=pres;
}
