/* Cruise Control
 */

#include <RedBot.h>

#define ECHO_PIN 10
#define TRIG_PIN 11
#define L_ENC_PIN A0
#define R_ENC_PIN A5
#define L_IR_PIN A2
#define R_IR_PIN A6
#define BUZZER 3

#define BAUDRATE 9600


// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
const int dist_stop =12;//in cm 
const int dist_safe = 30;//in cm
const int const_speed = 150;//+ve

RedBotMotors motors;
RedBotEncoder encoder = RedBotEncoder(A0, A5);

void initConfig(){
  //GPIO config //{A0,A1,A2,A3,A4,A5,A6,A7,3,9,10,11}
  // Ultrasonic Sensor HC-SR04
  pinMode(ECHO_PIN, INPUT_PULLUP);// echo_pin=10
  pinMode(TRIG_PIN, OUTPUT);// trig_pin=11
  pinMode(L_ENC_PIN, INPUT_PULLUP);// l_enc_pin=A0
  pinMode(R_ENC_PIN, INPUT_PULLUP);// r_enc_pin=A5
  pinMode(L_IR_PIN, INPUT_PULLUP);// l_ir_pin=A2
  pinMode(R_IR_PIN, INPUT_PULLUP);// r_ir_pin=A6
  
  pinMode(BUZZER, OUTPUT);
  
  //serial config
  Serial.begin(BAUDRATE);//baudrate=9600
  
}

int getDistanceUltrasonic()
{
  // Clears the TRIG_PIN condition
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  // Sets the TRIG_PIN HIGH (ACTIVE) for 10 microseconds
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  // Reads the ECHO_PIN, returns the sound wave travel time in microseconds
  duration = pulseIn(ECHO_PIN, HIGH);
  // Calculating the distance
  distance = duration * 0.0343 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm"); 

  return distance;
}

void decelerate(int current_speed, int new_speed)
{
  int delta = 0;
  if(current_speed > new_speed)
  {  
    delta = -1;
  }
  else
  {
    delta = 1;
  }
  
  while(current_speed != new_speed)
  {
    current_speed = current_speed + delta;
    //motors.drive(current_speed);
    driveStraight(20, current_speed);
    delay(5);//in msec
  }
}

void accelerate(int current_speed, int new_speed)
{
  int delta = 0;
  if(current_speed < new_speed)
  {  
    delta = 1;
  }
  else
  {
    delta = -1;
  }
  
  while(current_speed != new_speed)
  {
    current_speed = current_speed + delta;
    //motors.drive(current_speed);
    driveStraight(20, current_speed);
    delay(5);//in msec
  }
}

void driveStraight(float distance, int motorPower)
{
  const int countsPerRev = 192;   // 4 pairs of N-S x 48:1 gearbox = 192 ticks per wheel rev
    
  const float wheelDiam = 65;  // diam = 65mm / 25.4 mm/in
  const float wheelCirc = PI*wheelDiam;  // Redbot wheel circumference = pi*D
    
  long lCount = 0;
  long rCount = 0;
  long targetCount;
  float numRev;

  // variables for tracking the left and right encoder counts
  long prevlCount, prevrCount;

  long lDiff, rDiff;  // diff between current encoder count and previous count

  // variables for setting left and right motor power
  int leftPower = motorPower;
  int rightPower = motorPower;

  // variable used to offset motor power on right vs left to keep straight.
  int offset = 5;  // offset amount to compensate Right vs. Left drive

  numRev = distance / wheelCirc;  // calculate the target # of rotations
  targetCount = numRev * countsPerRev;    // calculate the target count
/*
  // debug
  Serial.print("driveStraight() ");
  Serial.print(distance);
  Serial.print(" cm at ");
  Serial.print(motorPower);
  Serial.println(" power.");

  Serial.print("Target: ");
  Serial.print(numRev, 3);
  Serial.println(" revolutions.");
  Serial.println();
  
  // print out header
  Serial.print("Left\t");   // "Left" and tab
  Serial.print("Right\t");  // "Right" and tab
  Serial.println("Target count");
  Serial.println("============================");
*/
  encoder.clearEnc(BOTH);    // clear the encoder count
  //delay(100);  // short delay before starting the motors.
  
  motors.drive(motorPower);  // start motors 

  while (rCount < targetCount)
  {
    // while the right encoder is less than the target count -- debug print 
    // the encoder values and wait -- this is a holding loop.
    lCount = encoder.getTicks(LEFT);
    rCount = encoder.getTicks(RIGHT);
/*    
    Serial.print(lCount);
    Serial.print("\t");
    Serial.print(rCount);
    Serial.print("\t");
    Serial.println(targetCount);
*/
    motors.leftDrive(leftPower);
    motors.rightDrive(rightPower);

    // calculate the rotation "speed" as a difference in the count from previous cycle.
    lDiff = (lCount - prevlCount);
    rDiff = (rCount - prevrCount);

    // store the current count as the "previous" count for the next cycle.
    prevlCount = lCount;
    prevrCount = rCount;

    // if left is faster than the right, slow down the left / speed up right
    if (lDiff > rDiff) 
    {
      leftPower = leftPower - offset;
      rightPower = rightPower + offset;
    }
    // if right is faster than the left, speed up the left / slow down right
    else if (lDiff < rDiff) 
    {
      leftPower = leftPower + offset;  
      rightPower = rightPower - offset;
    }
    //delay(50);  // short delay to give motors a chance to respond.
  }
  // now apply "brakes" to stop the motors.
  //motors.brake();  
}

void setup() {
  //pinMode(TRIG_PIN, OUTPUT); // Sets the TRIG_PIN as an OUTPUT
  //pinMode(ECHO_PIN, INPUT); // Sets the ECHO_PIN as an INPUT
  //Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  initConfig();

  //start motor
  motors.drive(const_speed);
  
  Serial.print("Cruise Control Test "); // print some text in Serial Monitor
  Serial.println("with Redbot mainboard");
}

void loop() {
  int dist_front = getDistanceUltrasonic();

  if(dist_front <= dist_stop)
  {
    //constant speed
    motors.brake();
  }
  else if(dist_front > dist_safe)
  {
    //accelerate
    accelerate(const_speed, const_speed+20);// considering const_speed is positive 
  }
  else if(dist_front < dist_safe)
  {
    //decelerate
    decelerate(const_speed, const_speed-20);// considering const_speed is positive 
  }
  else 
  {
    //motors.drive(const_speed);
    driveStraight(20, const_speed);
  }
}
