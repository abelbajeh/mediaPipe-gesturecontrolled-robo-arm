#include <Servo.h>

#define clawPin  11
#define rightSpin  10
#define leftSpin 6
#define basePin 5

int clawVal;
int rightSval;
int leftSval;
int baseVal;

String data;

Servo claw;
Servo rightS;
Servo leftS;
Servo baseS;

void setup(){
  Serial.begin(9600);
  claw.attach(clawPin);
  rightS.attach(rightSpin);
  leftS.attach(leftSpin);
  baseS.attach(basePin);
}
void loop(){
  if(Serial.available() > 1){
    data = Serial.readStringUntil('\n');
    data.trim();
    int a = data.indexOf(":");
    int b = data.indexOf(":", a+1);
    int c = data.indexOf(":", b+1);
    clawVal = data.substring(0,a).toInt();
    rightSval = data.substring(a+1, b).toInt();
    leftSval = data.substring(b+1, c).toInt();
    baseVal = data.substring(c+1).toInt();

    rightS.write(rightSval);
    claw.write(clawVal);
    leftS.write(leftSval);
    baseS.write(baseVal);
  }
  // leftS.write(100);
}