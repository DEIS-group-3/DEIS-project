/***********************************************************************
 * Using Accelerometer readings contril the speed of the robot.
 * Hardware setup:
 * You'll need to attach the RedBot Accelerometer board to hader on the upper
 * right side of the mainboard. See the manual for details on how to do this.
 ***********************************************************************/

#include <RedBot.h>
int motorPower = 80;  // variable for setting the drive power

#define ECHO_PIN 10
#define TRIG_PIN 11
#define L_ENC_PIN A0
#define R_ENC_PIN A1
#define L_IR_PIN A2
#define R_IR_PIN A6

#define SDA A4
#define SCL A5
#define BUZZER 3

#define BAUDRATE 9600

#define echoPin 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 11 //attach pin D3 Arduino to pin Trig of HC-SR04

// defines variables
const int self_robot_id = 4; //spiral code
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
const int const_speed = 100;
#define SPEED 128  // sets the nominal speed. Set to any number from 0 - 255.

RedBotMotors motors;
int leftSpeed;   // variable used to store the leftMotor speed
int rightSpeed;  // variable used to store the rightMotor speed

RedBotSensor left = RedBotSensor(A2); // initialize a sensor object on A3
RedBotSensor right = RedBotSensor(A6); // initialize a sensor object on A6

RedBotAccel accelerometer;

void initConfig(){
  //GPIO config //{A0,A1,A2,A3,A4,A5,A6,A7,3,9,10,11}
  // Ultrasonic Sensor HC-SR04
  pinMode(ECHO_PIN, INPUT_PULLUP);// echo_pin=10
  pinMode(TRIG_PIN, OUTPUT);// trig_pin=11
  pinMode(L_ENC_PIN, INPUT_PULLUP);// l_enc_pin=A0
  pinMode(R_ENC_PIN, INPUT_PULLUP);// r_enc_pin=A5
  pinMode(L_IR_PIN, INPUT_PULLUP);// l_ir_pin=A2
  pinMode(R_IR_PIN, INPUT_PULLUP);// r_ir_pin=A6

  pinMode(SCL, OUTPUT);// accelerometer clock pin
  pinMode(SDA, INPUT_PULLUP);// accelerometer data pin
  
  pinMode(BUZZER, OUTPUT);
  
  //serial config
  Serial.begin(BAUDRATE);//baudrate=9600
  
}
//RedBotMotors motors;

// The RedBot library includes support for the accelerometer. We've tried
// to make using the accelerometer as easy as to use as possible.


void setup(void)
{
  initConfig();
  Serial.begin(9600);
  
}

void loop(void)
{
  accelerometer.read(); // updates the x, y, and z axis readings on the acceleromter

  accelerometer.read(); // updates the x, y, and z axis readings on the accelerometer

  int xAccel = accelerometer.x;
  int yAccel = accelerometer.y;
  int zAccel = accelerometer.z;

  float XZ = accelerometer.angleXZ;  // read in the XZ angle
  float YZ = accelerometer.angleYZ;  // read in the YZ angle
  float XY = accelerometer.angleXY;  // read in the XY angle

  Serial.print(XZ, 2);  // prints out floating point number with 2 decimal places
  Serial.print("\t");   // tab
  Serial.println(motorPower);  // prints out motorPower

  if((XZ > 10) & (XZ < 21))
 {
    motors.drive(200);
  }
  else if(XZ < 8)
  {
    motors.drive(50);
  }
  else if((XZ < -8 ) & (XZ > -21 ))
  {
    motors.drive(10);
  }

}
