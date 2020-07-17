#include <Wire.h>
int prev3=5;
int prev2 =507;
int prev = 507;
float pres =507;
int soundRead;
int count=0;
void setup(){
  Serial.begin(9600);
}

void loop(){
  soundRead=analogRead(A3);
  //pres=soundRead*0.93+prev*0.07;
  if(abs(soundRead-(prev+prev2+prev3+2)/3)>4){//threshold
    count=400;
  }
  if(count>0){
    /*
    Serial.write(highByte(prev3));
    Serial.write(lowByte(prev3));
    Serial.write('\r');
    Serial.write('\n');*/
    byte sendMsg[3] = {highByte(prev3),lowByte(prev3),'\n'};
    Serial.write(sendMsg,3);
    count--;
  }
  prev3=prev2;
  prev2=prev;
  //prev=pres;
  prev=soundRead;
}
