#include <Wire.h>
int prev3=507;
int prev2 =507;
int prev = 507;
float pres =507;
int soundRead;
//int count=0;
unsigned timeoutCheck=0;
bool continuous=false;

void setup(){
  Serial.begin(9600);
}

void loop(){
  soundRead=analogRead(A3);
  //pres=soundRead*0.93+prev*0.07;
  if(!continuous && abs(soundRead-(prev+prev2+prev3+2)/3)>4){//threshold
    //count=400;
    //if(!continuous){
      Serial.write(0);
      continuous=true;
      timeoutCheck=0;
    //}
  }
  if(timeoutCheck<600){//(count>0 && timeoutCheck<600){
    byte sendMsg[3] = {highByte(prev3),lowByte(prev3),'\n'};
    Serial.write(sendMsg,3);
    //count--;
    timeoutCheck++;
  }else if(continuous){
    continuous=false;
    Serial.write(0);Serial.write(0);Serial.write(0);Serial.write(0);Serial.write('\n');
  }
  prev3=prev2;
  prev2=prev;
  //prev=pres;
  prev=soundRead;
}
