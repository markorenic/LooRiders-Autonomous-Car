//=======================================================
// specify fancy moves
//===============================================================
//#include <Servo.h> 
int Left_motor_back=6;       
int Left_motor_go=7;         

int Right_motor_go=9;       
int Right_motor_back=8;   

int Right_motor_en=10;      
int Left_motor_en=5;      

/*Set Button port*/
int key=13;

/*Set BUZZER port*/
int beep=12; 
void setup()
{
   //Initialize motor drive for output mode
  pinMode(Left_motor_go,OUTPUT); 
  pinMode(Left_motor_back,OUTPUT);
  pinMode(Right_motor_go,OUTPUT);
  pinMode(Right_motor_back,OUTPUT);
  pinMode(Right_motor_en,OUTPUT);
  pinMode(Left_motor_en,OUTPUT);
  pinMode(key,INPUT);// Set button as input
  pinMode(beep,OUTPUT);// Set buzzer as output
  digitalWrite(key,HIGH);//Initialize button
  digitalWrite(beep,LOW);// set buzzer mute
}
void run(int time)     // ahead
{
 digitalWrite(Left_motor_en,HIGH);  // Left motor enable
  analogWrite(Left_motor_en,255);
  digitalWrite(Right_motor_en,255);  // Right motor enable
  digitalWrite(Right_motor_go,HIGH);  // right motor go ahead
  digitalWrite(Right_motor_back,LOW);   
  analogWrite(Right_motor_go,255);//PWM--Pulse Width Modulation(0~255). right motor go speed is 255.
  analogWrite(Right_motor_back,0); 
  digitalWrite(Left_motor_go,HIGH);  // set left motor go ahead
  digitalWrite(Left_motor_back,LOW);
  analogWrite(Left_motor_go,130);//PWM--Pulse Width Modulation(0~255).left motor go speed is 135.
  analogWrite(Left_motor_back,0);
  delay(time * 100);   //Running time can be adjusted 
}

void brake(int time)         //STOP
{
  digitalWrite(Right_motor_go,LOW);//Stop the right motor
  digitalWrite(Right_motor_back,LOW);
  digitalWrite(Left_motor_go,LOW);//Stop the left motor
  digitalWrite(Left_motor_back,LOW);
  delay(time * 100);  //Running time can be adjusted  
}

void left(int time)        //turn left
{
  digitalWrite(Right_motor_go,HIGH);	// right motor go ahead
  digitalWrite(Right_motor_back,LOW);
  analogWrite(Right_motor_go,255); // PWM--Pulse Width Modulation(0~255) control speed，right motor go speed is 255.
  analogWrite(Right_motor_back,0);
  digitalWrite(Left_motor_go,LOW);   // left motor stop
  digitalWrite(Left_motor_back,LOW); 
  analogWrite(Left_motor_go,0); 
  analogWrite(Left_motor_back,0);
  delay(time * 100);	
}
void spin_left(int time)   //Left rotation
{
  digitalWrite(Right_motor_go,HIGH);// right motor go ahead
  digitalWrite(Right_motor_back,LOW);
  analogWrite(Right_motor_go,200);// PWM--Pulse Width Modulation(0~255) control speed ,right motor go speed is 200.
  analogWrite(Right_motor_back,0);
  digitalWrite(Left_motor_go,LOW);   // left motor back off
  digitalWrite(Left_motor_back,HIGH);
  analogWrite(Left_motor_go,0); 
  analogWrite(Left_motor_back,200);// PWM--Pulse Width Modulation(0~255) control speed,left motor back speed is 200.
  delay(time * 100);
}

void right(int time)      //turn right
{
 digitalWrite(Right_motor_go,LOW);   // right motor stop
  digitalWrite(Right_motor_back,LOW);
  analogWrite(Right_motor_go,0); 
  analogWrite(Right_motor_back,0);
  digitalWrite(Left_motor_go,HIGH);// left motor go ahead
  digitalWrite(Left_motor_back,LOW);
  analogWrite(Left_motor_go,130);// PWM--Pulse Width Modulation(0~255) control speed ,left motor go speed is 255.
  analogWrite(Left_motor_back,0);
  delay(time * 100);
}

void spin_right(int time)   //Right rotation
{
  digitalWrite(Right_motor_go,LOW);  // right motor back off
  digitalWrite(Right_motor_back,HIGH);
  analogWrite(Right_motor_go,0); 
  analogWrite(Right_motor_back,200);// PWM--Pulse Width Modulation(0~255) control speed
  digitalWrite(Left_motor_go,HIGH);// left motor go ahead
  digitalWrite(Left_motor_back,LOW);
  analogWrite(Left_motor_go,200);// PWM--Pulse Width Modulation(0~255) control speed 
  analogWrite(Left_motor_back,0);
  delay(time * 100);
}

void back(int time)   //back off 
{
  digitalWrite(Right_motor_go,LOW); //right motor back off
  digitalWrite(Right_motor_back,HIGH);
  analogWrite(Right_motor_go,0);
  analogWrite(Right_motor_back,255);// PWM--Pulse Width Modulation(0~255) control speed
  analogWrite(Right_motor_en,240);
  digitalWrite(Left_motor_go,LOW);  //left motor back off
  digitalWrite(Left_motor_back,HIGH);
  analogWrite(Left_motor_go,0);
  analogWrite(Left_motor_back,247);// PWM--Pulse Width Modulation(0~255) control speed
  delay(time * 100);
}
void keysacn()
{
  int val;   
  val=digitalRead(key);// Reads the button ,the level value assigns to val
  while(digitalRead(key))// When the button is not pressed
  {
    val=digitalRead(key);
  }
  while(!digitalRead(key))// When the button is pressed
  {
    delay(10);	//delay 10ms
    val=digitalRead(key);// Reads the button ,the level value assigns to val
    if(val==LOW)  //Double check the button is pressed
    {
       
      digitalWrite(beep,HIGH);//The buzzer sounds
      delay(50);//delay 50ms
      while(!digitalRead(key))	//Determine if the button is released or not
        digitalWrite(beep,LOW);//mute
    }
    else
      digitalWrite(beep,LOW);//mute
  }
}

/*main loop*/

void loop()
{    
   
  keysacn();//Press the button to start
  while(1)
 { 
  run(10);//10*100ms=1s  ahead 1s
  back(10);//back 1s
  brake(5);//5*100ms=500ms=0.5s  brake 0.5s
   int i;
  for(i=0;i<5;i++)
  {
    run(10);//The car moved forward five times
    brake(2);//brake  0.2s
  }

  for(i=0;i<5;i++)
  {
    back(10);//The car moved back five times
    brake(2);//brake 0.2s
  }

  for(i=0;i<5;i++)
  {
    left(10);//Turn left 5 times and rotate left
    spin_left(5);
  }

  for(i=0;i<5;i++)
  {
    right(10);//Turn right 5 times and rotate right
    spin_right(5);
  }

  for(i=0;i<10;i++)
  {
    right(1);//Turn right 10 times in the right place
    brake(1);
  }

  for(i=0;i<10;i++)
  {
    left(1);//Turn left 10 times in the right place
    brake(1);
  }

  for(i=0;i<10;i++)
  {
    left(3);//Go S ,turn left 0.3 s
    right(3);//turn right 0.3 s
  }

  for(i=0;i<10;i++)
  {
    spin_left(3);//rotate left
    brake(3);//stop 0.3s
  }

  for(i=0;i<10;i++)
  {
    spin_right(3);//rotate right
    brake(3);//stop 0.3s
  }

}
}
