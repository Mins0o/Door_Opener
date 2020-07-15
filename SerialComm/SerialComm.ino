#include <Wire.h>
int prev = 500;
int pres;
byte soundRead;

void setup(){
  Serial.begin(9600);
}

void loop(){
  soundRead=analogRead(A3);
  pres=prev*0.6+soundRead*0.4;
  Serial.println(pres);
  prev=pres;
}
