
#include <RedBot.h>
RedBotSensor left = RedBotSensor(A2); // initialize a sensor object on A3
RedBotSensor right = RedBotSensor(A6); // initialize a sensor object on A6

//#define MINTHRESHOLD 700
//#define MAXTHRESHOLD 1000
#define SPEED 128  // sets the nominal speed. Set to any number from 0 - 255.

RedBotMotors motors;
int leftSpeed;   // variable used to store the leftMotor speed
int rightSpeed;  // variable used to store the rightMotor speed

void setup()
{
    Serial.begin(9600);
    Serial.println("Welcome to experiment 6.2 - Line Following");
    Serial.println("------------------------------------------");
    motors.drive(SPEED);
    //delay(5000);
    Serial.println("IR Sensor Readings: ");
    delay(10);
}

void loop()
{
    int leftread, rightread;
    leftread = left.read();
    rightread = right.read();
    
    Serial.print(leftread);
    Serial.print("\t");  // tab character
    Serial.print(rightread);
    Serial.println();

    leftSpeed = SPEED;
    rightSpeed = SPEED;
/*
    if(rightread >= 800)
    {
        leftSpeed = 0;
        rightSpeed = SPEED + 10;
    }

    // if the line is under the left sensor, adjust relative speeds to turn to the left
    if(leftread >= 800)
    {
        leftSpeed = SPEED + 10;
        rightSpeed = 0;
    }
*/
    if((leftread > 1000)  && (rightread > 1000) )
    {
      motors.stop();
    }
    if((leftread >= 900) && (rightread < 650))
    {
      //turn right
      motors.leftMotor(0);
      motors.rightMotor(-0.3*SPEED);
    }
    if((rightread >= 900) && (leftread < 650))
    {
      //turn left
      motors.leftMotor(0.3*SPEED);
      motors.rightMotor(0);      
    }
    if((leftread < 650)  && (rightread < 650))
    {
       motors.drive(SPEED);
    }
    /*
    else
    {
      motors.leftMotor(leftSpeed);
      motors.rightMotor(rightSpeed);
    }
    */
    delay(0);  // add a delay to decrease sensitivity.*/
}
