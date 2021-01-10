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
const int const_speed = 200;//+ve

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

void setup() {
  // put your setup code here, to run once:
    initConfig();
    Serial.println("Automated driving at a slope...");
    delay(500);
}

void loop() {
  Serial.println("START");
  //forward
  motors.drive(const_speed);
  delay(2100);
  
  //turn left
  motors.leftMotor(0.35*const_speed);
  motors.rightMotor(0.35*const_speed);
  delay(1500);
  
  //forward - bridge
  motors.drive(const_speed);
  delay(2200);

    
  //turn left
  motors.leftMotor(0.35*const_speed);
  motors.rightMotor(0.35*const_speed);
  delay(1500);

    
  //forward
  motors.drive(const_speed);
  delay(2100);

  //stop
  motors.brake();

  Serial.println("STOP");
  while(1);
}
