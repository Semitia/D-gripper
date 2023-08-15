#include<SCoop.h>

const int A1_pin=3,A2_pin=4,B1_pin=5,B2_pin=6, LED_pin=13;
const int next[5] = {0,4,3,1,2},
          last[5] = {0,3,4,2,1};

/**
 * 信息打印线程
*/
defineTaskLoop(info_Task){
  static bool LED_state = 1;
  while(1){
    Serial.println("hello");
    // delay(2000); 针对全局
    sleep(2000); // 针对线程
    if(LED_state) {
      LED_state=0;
      digitalWrite(LED_pin,HIGH);
    }
    else {
      digitalWrite(LED_pin,LOW);
      LED_state=1;   
    }
  }
}

void setup() {
  pinMode(A1_pin,OUTPUT);
  pinMode(A2_pin,OUTPUT);
  pinMode(B1_pin,OUTPUT);
  pinMode(B2_pin,OUTPUT);
  pinMode(LED_pin,OUTPUT);
  Serial.begin(115200);
  while(Serial.read()>=0){}//clear buffer
  mySCoop.start();
}

void set_step(int ID)
{
  switch(ID){
    case 1:
      //Serial.println("mode 1");
      digitalWrite(A1_pin,HIGH);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,LOW);
      break;
    case 2:
      //Serial.println("mode 2");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,HIGH);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,LOW);
      break;
    case 3:
      //Serial.println("mode 3");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,HIGH);
      digitalWrite(B2_pin,LOW);
      break;
    case 4:
      //Serial.println("mode 4");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,HIGH);
      break;
    case 0:
      //Serial.println("stop");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,LOW);
      break;
    case 5:
      //Serial.println("mode5");
      digitalWrite(A1_pin,HIGH);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,HIGH);
      digitalWrite(B2_pin,LOW);
      break;
    case 6:
      //Serial.println("mode6");
      digitalWrite(A1_pin,HIGH);
      digitalWrite(A2_pin,LOW);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,HIGH);
      break;
    case 7:
      //Serial.println("mode7");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,HIGH);
      digitalWrite(B1_pin,LOW);
      digitalWrite(B2_pin,HIGH);
      break;
    case 8:
      //Serial.println("mode8");
      digitalWrite(A1_pin,LOW);
      digitalWrite(A2_pin,HIGH);
      digitalWrite(B1_pin,HIGH);
      digitalWrite(B2_pin,LOW);
      break;                        
    default:
      Serial.println("Invalid input");
      break;
    }
    return;
}

void set_motor(int delay_ms, bool dir)
{
  static int tem_step=1;
  
  if(dir) {
    tem_step=next[tem_step];
    set_step(tem_step);
  }

  else {
    tem_step=last[tem_step];
    set_step(tem_step);
  }
  delay(delay_ms);
  
  return;
}

static int freq=10;
static bool dir=1;
void loop() {

  set_motor(freq,dir);

  yield();
}

/*
serialEvent是一种在接收到串口数据时自动调用的函数，它可以让你在loop()函数执行完后处理串口数据。
serialEvent会在每次loop()函数结束时被检查，如果串口缓冲区中有可用的数据，就会触发serialEvent。
你可以使用Serial.read()等函数来读取串口数据，并进行相应的操作。
如果你的板子有多个串口，你也可以使用serialEvent1()，serialEvent2()等函数来分别处理不同的串口数据。
*/
void serialEvent(){
  static int buf_index=0, end_flag=0;
  while(Serial.available()>0)
  {
    uint8_t data=Serial.read();

  }
}
