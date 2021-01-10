
#include <RedBot.h>

#define ECHO_PIN 10
#define TRIG_PIN 11
#define L_ENC_PIN A0
#define R_ENC_PIN A5
#define L_IR_PIN A2
#define R_IR_PIN A6
#define BUZZER 3

#define BAUDRATE 9600

#define echoPin 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 11 //attach pin D3 Arduino to pin Trig of HC-SR04

// defines variables
const int self_robot_id = 4; //spiral code
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
const int const_speed = 100;


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

void setup() {
  //Serial.begin(9600);
  initConfig();
  Serial.print("Ultrasonic Sensor HC-SR04 Test "); // print some text in Serial Monitor
  Serial.println("with Redbot mainboard");
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

void loop() {
//Serial.println("----------START----------");

/*//TESTING
    String data = "1,temp data; ok.";
Serial.println("BEF:data");
Serial.println(data);
//    int data_len = data.length();
//    char data_buf[data_len];
//    data.toCharArray(data_buf, data_len);
//Serial.println("BEF:data_buf");
//Serial.println(data_buf);

String data_pkt[10];
    parseData(data, data_pkt);

Serial.println("AFT:data_pkt");
Serial.println(data_pkt[0]);
Serial.println(data_pkt[1]);
Serial.println(data_pkt[2]);
Serial.println(data_pkt[3]);

Serial.println("AFT:data");
Serial.println(data);
    delay(2000);
*/

  if (Serial.available() > 0) 
  {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);

    String data_pkt[20];
    parseData(data, data_pkt);

//Serial.print("AFT:data_pkt");
//Serial.print(data_pkt[0]);//timestamp
//Serial.print(data_pkt[1]);//action_id
//Serial.print(data_pkt[2]);//source_robot_id
//Serial.print(data_pkt[3]);//target_platoon_id
//Serial.print(data_pkt[4]);//target_robot_id
//Serial.print(data_pkt[5]);//left speed
//Serial.print(data_pkt[6]);//right speed
//Serial.println(data_pkt[7]);//

//Serial.println("AFT:data");
//Serial.println(data);

    if(data_pkt[4].toInt() == self_robot_id || data_pkt[4].toInt() == -2){
      switch(data_pkt[1].charAt(0)){
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
          int lspeed = data_pkt[5].toInt();
          //Serial.println(lspeed);
          int rspeed = data_pkt[6].toInt();
          //Serial.println(rspeed);
          //motors.drive(lspeed);
          motors.leftDrive(lspeed);
          motors.rightDrive(rspeed);

          //Serial.print(data_pkt[4]);//target_robot_id
          Serial.print(data_pkt[5]);//left speed
          Serial.println(data_pkt[6]);//right speed
          Serial.println(data_pkt[7]);//

          break;
        }//case end
        default:
        {
          motors.drive(255);
          break;
        }
      }//SWITCH END

    }
  }

//Serial.println("----------END----------"); 
//while(1);
}
