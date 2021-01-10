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
const int dist_stop = 30;//in cm 
const int dist_safe = 80;//in cm
const int const_speed = 150;//+ve

RedBotMotors motors;

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
    motors.drive(current_speed);
    delay(10);//in msec
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
    motors.drive(current_speed);
    delay(10);//in msec
  }
}

void setup() {
  //pinMode(TRIG_PIN, OUTPUT); // Sets the TRIG_PIN as an OUTPUT
  //pinMode(ECHO_PIN, INPUT); // Sets the ECHO_PIN as an INPUT
  //Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  initConfig();

  //start motor
  motors.drive(const_speed);
  delay(1000);
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
    accelerate(const_speed, const_speed+50);// considering const_speed is positive 
  }
  else if(dist_front < dist_safe)
  {
    //decelerate
    decelerate(const_speed, const_speed-50);// considering const_speed is positive 
  }
  else 
  {
    motors.drive(const_speed);
  }
}
