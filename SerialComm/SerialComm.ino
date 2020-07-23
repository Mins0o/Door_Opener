#include <Wire.h>
#include <Stepper.h>
#include <Servo.h>
int prev3=507;
int prev2 =507;
int prev = 507;
float pres =507;
int soundRead;
//int count=0;
unsigned timeoutCheck=0;
volatile bool openDoor=false;
bool continuous=false;
const int stepsPerRound=2048;
Stepper handlePuller(stepsPerRound,5,7,6,8);

void setup(){
  Wire.begin(0x8);
  Wire.onReceive(receiveEvent);
  handlePuller.setSpeed(12);
  handlePuller.step(1000);
  pinMode(13,OUTPUT);
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
  if(openDoor){
    Wire.read();
    digitalWrite(13,HIGH);
    handlePuller.step(-2000);
    digitalWrite(13,LOW);
    openDoor=false;
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

void receiveEvent(){
  while(Wire.available()){
    Wire.read();
  }
  openDoor=true;
}
