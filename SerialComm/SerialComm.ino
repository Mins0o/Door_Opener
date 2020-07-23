#include <Wire.h>
#include <Stepper.h>
#include <Servo.h>

// These three variables to store three past read values
int prev3=507; int prev2 =507; int prev = 507;

// This variable is used for filtering
//float pres=507;

// The analog input value from the microphone
int soundRead;

// To keep the "sound snippet" within certain length
unsigned timeoutCheck=0;

// This variable is responsible of handling the actuation according to the signal the RPi sent.
// Since the signal is sent by I2C and arduino can only handle one ISR at a time, we use volatile variable to keep track of it.
volatile bool openDoor=false;

// To check the start and end of the "sound snippet"
bool continuous=false;

//setting up stepper and servo
const int stepsPerRound=2048;
Stepper handlePuller(stepsPerRound,5,7,6,8);
Servo doorPusher;

void setup(){
  //I2C bus address 0x8 and receive handler
  Wire.begin(0x8);
  Wire.onReceive(receiveEvent);

  //motors
  doorPusher.attach(9);
  //doorPusher.write(10);
  delay(100);
  handlePuller.setSpeed(12);
  //handlePuller.step(1000);

  //pin 13 is to check if the actuation routine is being executed.
  pinMode(13,OUTPUT);
  Serial.begin(9600);
}

void loop(){
  if(openDoor){// this part of the code gets executed if 'openDoor' variable is set true in the receive handler.
    // actuation part
    digitalWrite(13,HIGH);
    handlePuller.step(-2*stepsPerRound);
    doorPusher.write(90);
    delay(500);
    doorPusher.write(0);
    delay(500);
    handlePuller.step(2*stepsPerRound);
    digitalWrite(13,LOW);
    openDoor=false;
  }
  
  soundRead=analogRead(A3);
  
  //pres=soundRead*0.93+prev*0.07;

  // If a sound passes the threshold, send it to RPi for inspection a.k.a. classification
  if(!continuous && abs(soundRead-(prev+prev2+prev3+2)/3)>4){//threshold
      // Because of this, the start of the sound snippet will be len4
      Serial.write(0);
      continuous=true;
      timeoutCheck=0;
  }

  // Keep writing integer(2bytes) and a newline(1byte) to the serial until time runs out
  if(timeoutCheck<150){
    byte sendMsg[3] = {highByte(prev3),lowByte(prev3),'\n'};
    Serial.write(sendMsg,3);
    timeoutCheck++;
  }else if(continuous){// If time ran out but arduino was sending signal till last loop(), mark end of the "sound snippet"
    continuous=false;
    Serial.write(0);Serial.write(0);Serial.write(0);Serial.write(0);Serial.write('\n');
  }

  // Store three past values
  prev3=prev2;
  prev2=prev;
  //prev=pres;
  prev=soundRead;
  // and read new at the satrt of the loop()
}

void receiveEvent(){
  char hey;
  while(Wire.available()){ // Flush any I2C from RPi
    hey=Wire.read();
  }
  if (hey=1){openDoor=true;} // This will take efect at the start of the loop()
}
