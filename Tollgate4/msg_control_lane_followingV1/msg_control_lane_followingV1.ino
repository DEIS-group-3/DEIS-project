/*
 Message control Lane following V1
*/


#include <RedBot.h>

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

void followLane(const int newSPEED)
{
    int leftread, rightread;
    leftread = left.read();
    rightread = right.read();
    
    //Serial.print(leftread);
    //Serial.print("\t");  // tab character
    //Serial.print(rightread);
    //Serial.println();

    leftSpeed = newSPEED;
    rightSpeed = newSPEED;

    if((leftread > 1000)  && (rightread > 1000) )
    {
      motors.stop();
    }
    if((leftread >= 900) && (rightread < 650))
    {
      //turn right
      motors.leftMotor(0);
      motors.rightMotor(-0.3*newSPEED);
    }
    if((rightread >= 900) && (leftread < 650))
    {
      //turn left
      motors.leftMotor(0.3*newSPEED);
      motors.rightMotor(0);      
    }
    if((leftread < 650)  && (rightread < 650))
    {
       motors.drive(newSPEED);
    }
    delay(0);  // add a delay to decrease sensitivity.*/
}

void action(const char action_id, const int msg1, const int msg2, const int msg3){
        switch(action_id){
        //Serial.println(data_pkt[1].charAt(0));
        case 'a':
        {  
          break;
        }
        case 'b':
        {  
          break;
        }
        case 'c':
        {  
          break;
        }
        case 'g':
        {        
//Serial.println("lspeed&rspeed");
          int lspeed = msg1; //data_pkt[5].toInt();
          //Serial.println(lspeed);
          int rspeed = msg2; //data_pkt[6].toInt();
          //Serial.println(rspeed);
          //motors.drive(lspeed);
          motors.leftDrive(lspeed);
          motors.rightDrive(rspeed);

          //Serial.print(msg1/*data_pkt[5]*/);//left speed
          //Serial.println(msg2/*data_pkt[6]*/);//right speed

          break;
        }//case end
        case 'j':
        {
          //if NO TURN -> GO straight
          if(msg1 == 0)
          {
           // Perform lane following using IR sensors
           // Activate IR sensors and keep in straight by controlling motor speeds 
              followLane(msg3);
           //
          }
          else//msg1 == 1 //ROTATE ENABLED
          {
            //rotate as per rotation angle (given as msg2)
          }

          break;
        }
        
        default:
        {
          motors.drive(255);
          break;
        }
      }//SWITCH END
}

void setup() {
  //Serial.begin(9600);
  initConfig();
  //Serial.print("Message control Lane following V1"); // print some text in Serial Monitor
  //Serial.println("");
}

void loop() {


  if (Serial.available() > 0) 
  {
    String data = Serial.readString();
//    String data = Serial.readStringUntil('\n');
    //Serial.print("You sent me: ");
    //Serial.println(data);

    String data_pkt[20];
    parseData(data, data_pkt);

    if(data_pkt[4].toInt() == self_robot_id || data_pkt[4].toInt() == -2)
    {
      action(data_pkt[1].charAt(0), data_pkt[5].toInt(), data_pkt[6].toInt(), data_pkt[7].toInt());
    }
  }
}
