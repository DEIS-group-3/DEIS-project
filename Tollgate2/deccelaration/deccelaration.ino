#include<RedBot.h>

RedBotMotors motors;


void setup() {
  // put your setup code here, to run once:
  //Consider the diffrent secnarios input here ( as of now dummy values are taken)
   Serial.begin(9600);

}



void loop() {
  int val; 
  // put your main code here, to run repeatedly:
 if (Serial.available()){
    val = Serial.read();
  }

  if(val == 1) // osbstacle
  {
    motors.stop(); // gradually stop the motor
  }
  else if( val == 2) // suddenobstacle
  {
    motors.brake();
  }
  else if(val == 3) // driveforword
  {
    motors.drive(127);
  }
  else if( val == 4) //drivereverse
  {
    motors.drive(-127);
  }
  else if(val == 5) //drivefordurationFw
  {
    motors.drive(127, 200);
  }
  else if(val == 6) // drivefordurationBw
  {
    motors.drive(-127, 200);
  }
  else if(val == 7) // trunrobotcw
  {
    motors.pivot(50);
  }
  else if(val == 8) // trunrobotccw
  {
    motors.pivot(-50);
  }
  else if(val == 9) // Deccelration
  {
    //motors.Decelaration(127);
  }
  else if(val == 10) // Acceleration 
  {
    //motors.Acceleration(127);
  }
  
  

  
  
}
