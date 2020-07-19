#include <Wire.h>

int piezoReading = 500;
int prev=500;
int pres=0;


int wprev=40;
int wpres=100-wprev;
void setup() {
  Serial.begin(9600);
  Wire.begin(0x8);
}

void loop() {
  piezoReading=analogRead(A1);
  pres=prev*(wprev/100.0)+piezoReading*(wpres/100.0);
  Serial.println(pres);
  Wire.println(pres);
  prev=pres;
}
