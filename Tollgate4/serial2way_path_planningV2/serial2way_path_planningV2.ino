//#ifndef CONFIG1
//#define CONFIG1


#include <RedBot.h>


#define ECHO_PIN 10
#define TRIG_PIN 11
#define L_ENC_PIN A0
#define R_ENC_PIN A1
#define L_IR_PIN A2
#define R_IR_PIN A6
#define L2_IR_PIN A3
#define R2_IR_PIN A7

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
const int dist_stop = 30;//in cm 
const int dist_safe = 80;//in cm
const int const_speed = 100;
#define SPEED 128  // sets the nominal speed. Set to any number from 0 - 255.

RedBotMotors motors;
int leftSpeed;   // variable used to store the leftMotor speed
int rightSpeed;  // variable used to store the rightMotor speed

RedBotSensor left = RedBotSensor(L_IR_PIN); // initialize a sensor object on A3
RedBotSensor right = RedBotSensor(R_IR_PIN); // initialize a sensor object on A6
int leftread, rightread;
RedBotSensor left2 = RedBotSensor(L2_IR_PIN); // initialize a sensor object on A3
RedBotSensor right2 = RedBotSensor(R2_IR_PIN); // initialize a sensor object on A6
int left2read, right2read;

//int jncount;
int Ljncount = 0, Rjncount = 0;

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
  //Serial.begin(BAUDRATE);//baudrate=9600
  
  Ljncount = 0; Rjncount = 0;
}

void m_brake()
{
    motors.brake();
    delay(250);
}
void turnLeft90()
{
    motors.brake(); //while(true);
    delay(250);
    //turn left 90 degrees
    motors.leftMotor(229);
    motors.rightMotor(229);//0
    delay(250);
    motors.brake(); //while(true);
}

void turnRight90()
{
    motors.brake(); //while(true);
    delay(250);
    //turn right 90 degrees
    motors.leftMotor(-229);//0
    motors.rightMotor(-229);
    delay(250);
    motors.brake(); //while(true);
}

void followLane()
{
    //int leftread, rightread;
    leftread = left.read();
    rightread = right.read();

    //int left2read, right2read;
    left2read = left2.read();
    right2read = right2.read();
/*    
    Serial.print(leftread);
    Serial.print("\t");  // tab character
    Serial.print(rightread);
    Serial.print("\t");  // tab character
    Serial.print(left2read);
    Serial.print("\t");  // tab character
    Serial.print(right2read);
    Serial.println();
*/
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
    if(((left2read < 650) || (leftread >= 900)) && (rightread < 650))
    {
      //turn right
      motors.leftMotor(-SPEED/4);//0 //32@128speed
      motors.rightMotor(-SPEED/2);////64@128speed
    }
    if(((right2read < 650) || (rightread >= 900)) && (leftread < 650))
    {
      //turn left
      motors.leftMotor(SPEED/2);////64@128speed
      motors.rightMotor(SPEED/4);//0 //32@128speed
    }
    if((leftread < 650)  && (rightread < 650))
    {
      //go forward
       motors.drive(SPEED);
    }
/*  //Need to update
    if((leftread < 650)  && (rightread < 650) && (left2read < 650)  && (right2read < 650))
    {
      //turn left
      motors.leftMotor(SPEED/2);
      motors.rightMotor(SPEED/4);
      delay(2);
      //go forward
      motors.drive(SPEED);
      delay(5);
      //turn right
      motors.leftMotor(-SPEED/4);
      motors.rightMotor(-SPEED/2);
      delay(2);
    }
 */
 
    /*
    else
    {
      motors.leftMotor(leftSpeed);
      motors.rightMotor(rightSpeed);
    }
    */
}

//NEED TO MODIFY
int detectIntersection()
{
  //static int Ljncount = 0, Rjncount = 0;
  int intersectionAt = 0;
  if((rightread < 650) && (right2read < 650))
  {
    //intersection detected and passage on right
      Rjncount++;
      if(Rjncount > 550)//55@128speed
      {
        intersectionAt = 1;
        //Serial.println("Passage on RIGHT");
        Rjncount = 0;
      }
      else
      {
        Ljncount = 0; Rjncount = 0;//TEMP
      }
  }
  else if((leftread < 650)  && (left2read < 650))
  {
    //intersection detected and passage on left
      Ljncount++;
      if(Ljncount > 550)//55@128speed
      {
        intersectionAt = -1;
        //Serial.println("Passage on LEFT");
        Ljncount = 0;
      }
      else
      {
        Ljncount = 0; Rjncount = 0;//TEMP
      }
  }

  if((left2read > 800))
  {
     Ljncount = 0;
  }
  if((right2read > 800))
  {
     Rjncount = 0; 
  }

  return intersectionAt;
}

void action(char act)
{
  switch(act)
  {
    case 'f'://Go straight
      motors.leftMotor(-SPEED);//TEST
      motors.rightMotor(SPEED);//TEST
      //followLane();
      break;
    case 'b'://Go back
      motors.drive(-200);
      break;
    case 'l'://Turn Left 90
      turnLeft90();
      //while(1);//TEST
      break;
    case 'r'://Turn Right 90
      turnRight90();
      //while(1);//TEST
      break;
    case 's'://brake
      m_brake();
      //while(1);//TEST
      break;
    default:
      m_brake();
      //while(1);//TEST
      break;
  }
}

char decideAction(int v)
{
  char z;
  if(v == 0)
  {
    z = 'f';//forward
  }
  else if(v == -1)
  {
    z = 'l';//left 90
  }
  else if(v == 1)
  {
    z = 'r';//right 90
  }
  else
  {
    z = 's';//stop
  }

  return z;
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
  //Serial.print("Distance: ");
  //Serial.print(distance);
  //Serial.println(" cm"); 

  return distance;
}

void avoidCollisionUS()
{
    // COLLISION AVOIDANCE
    int dist_front = getDistanceUltrasonic();

    if(dist_front <= dist_stop)
    {
      //constant speed
      motors.brake();
    }  
}

bool jn_flag = false;
bool isIntersection(int jn_nb)
{
  if(jn_nb == 0)
  {
    //Serial.println("NO INTERSECTION");
    return false;
  }
  else
  {
    //Serial.println("INTERSECTION");
    return true;
  }
  
  return false;
}

//#endif //CONFIG1
void parseData(String data, String data_pkt[])
{
  int index = 0;
  int data_len = data.length()+1;
  char str[data_len];
  data.toCharArray(str, data_len); 
  char * pch;
  //printf ("Splitting string \"%s\" into tokens:\n",str);
  pch = strtok (str," ,;");
  while (pch != NULL)
  {
    //printf ("%s\n",pch);
    data_pkt[index] = pch;
    pch = strtok (NULL, " ,;");

//Serial.print("new data_pkt: ");
//Serial.println(data_pkt[index]);

    index++;
  }
}

String pipeline;
void setup()
{
  
  initConfig();
  //pipeline = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffrfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff";//"---+r-";//TEST DUMMY
  //Serial.println("SETUP");
  //Serial.println(pipeline);
}

void appendPipeline(String newMsg[])
{
  for(int it = 0; it < 10; it++)
  {
    //Serial.print(" newit=");
    //Serial.println(newMsg[it]);
    //append(pipeline, newMsg[it]);
    pipeline+=newMsg[it];
  }
}

void updatePipeline(String newMsg[])
{
  if(newMsg[0] == "z" || newMsg[0] == "Z")
  {
    //Serial.println("--CLEAR & APPEND AT END--");
    pipeline = "";
    appendPipeline(newMsg);
    pipeline.remove(0,1); // m_dequeue();
    //Serial.println("---------");
  }
  else
  {
    //Serial.println("--APPEND AT END--");
    appendPipeline(newMsg);
    //Serial.println("---------");
  }
}

void m_enqueue(char ch)
{
  pipeline += ch;

  return;
}

char m_dequeue()
{
  //bool canDQ = false;
  char ch;
  if(pipeline == "")
  {
    //Serial.println("pipeline is empty!");
    ch = 'z';
  }
  else
  {
    ch = pipeline.charAt(0);
    //Serial.println(ch);
    pipeline.remove(0,1);
    //Serial.println(pipeline);
  }

  return ch;
}

void loop() {
  //Serial.println("LOOP START"); 
   //motors.drive(255);
//action('b');//TEST
//delay(1000);
   
//  if (Serial.available() > 0) 
  {
//    String data = Serial.readString();
    String data = Serial.readStringUntil('\n');
    //Serial.print("You sent me: ");
    //Serial.write(data[0]);
    //action('b');//TEST
//    String data_pkt[10];
//    parseData(data, data_pkt);
//    updatePipeline(data_pkt);
    //Serial.println(pipeline);
m_enqueue('s');//TEST
m_enqueue('s');//TEST
m_enqueue('l');//TEST
m_enqueue('l');//TEST
m_enqueue('s');//TEST
m_enqueue('s');//TEST
    //m_enqueue('b');//TEST
    //Serial.println(m_dequeue());//TEST
  } 
  //motors.drive(-255);
  //delay(1000);
  action(m_dequeue());
  //delay(2000);
  avoidCollisionUS();

  
/*
  do
  {
    action('f');//TEST
    avoidCollisionUS();
  }while(m_dequeue() != '+');

  action(m_dequeue());
*/
  
/*  
//  action(m_dequeue());//TEST
//jn_flag = true;//TEST; default=false
  //char c = m_dequeue();//TEST
  if(!jn_flag)
  //if(detectIntersection()==0 && c == 'f')
  {
    //static char c = pipeline=="" ? 's':m_dequeue();
    //c=='f'? action(c) : action('s');//expecting 'f' or 's'
    action('f');//TEST
    action('f');//TEST
    action('f');//TEST
    avoidCollisionUS();
    delay(2000);//TEST
    jn_flag = true;
  }
  else
  {
    action(m_dequeue());//expecting forward/turn followed by forward
    avoidCollisionUS();
  }
*/
   //Serial.println("LOOP END");  
  //delay(2);//0
  
}
