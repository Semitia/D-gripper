#include<SCoop.h>
#define MAX_POSITION 2600
const int A1_pin=3,A2_pin=4,B1_pin=5,B2_pin=6, LED_pin=13;

/**
 * 信息打印线程
*/
defineTaskLoop(info_Task){
  static bool LED_state = 1;
  while(1){
    //Serial.println("hello");
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

/**
 * 单步控制函数
*/
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


uint16_t position=0, target_pos=0;
static int freq=10;
const short next[5] = {0,4,3,1,2},
          last[5] = {0,3,4,2,1};
void set_speed(int delay_ms, bool dir)
{
  static int tem_step=1;

  if(dir) {
    tem_step=next[tem_step];
    set_step(tem_step);
    if(position==MAX_POSITION) position=0;
    else position++;
  }
  else {
    tem_step=last[tem_step];
    set_step(tem_step);
    if(position==0) position=MAX_POSITION;
    else position--;
  }

  delay(delay_ms);
  return;
}

void set_position(uint16_t tar_pos)
{
  int dis = tar_pos-position;
  if(dis==0) return;
  if(dis > 0){
    if(dis < MAX_POSITION/2) {
      set_speed(freq,1);
    }
    else set_speed(freq,0);
  }
  else {
    if(-dis < MAX_POSITION/2) {
      set_speed(freq,0);
    }
    else set_speed(freq,1);
  }
  return;
}

static bool dir=1, ctrl_mode=0;//0:position 1:speed
void loop() {
  if(ctrl_mode) set_speed(freq,dir);
  else set_position(target_pos);
  //yield();
}

/**
 * 串口数据处理函数，四种消息类型
 * @param buf 串口数据
 * byte 0：类型标识
 *  0x01设置速度
 *    byte 1：方向
 *    byte 2~3：速度大小，现在其实是步进时间间隔
 *  0x02设置位置
 *    byte 1~2：坐标
 *  0x03读取速度
 *  0x04读取位置
 *  0x05 stop
 *  0x06 position reset
*/  
void buf_process(uint8_t *buf)
{
  uint8_t type=buf[0];
  switch(type){
    case 0x01:
      dir=buf[1];
      freq=buf[2]<<8|buf[3];
      ctrl_mode=1;
      Serial.print("set speed: ");
      Serial.print(dir);
      Serial.print(" ");
      Serial.println(freq);
      break;
    case 0x02:
      target_pos=buf[1]<<8|buf[2];
      ctrl_mode=0;
      Serial.print("set target position: ");
      Serial.println(target_pos);
      break;
    case 0x03:
      Serial.println("read speed: ");
      Serial.print(dir);
      Serial.print(" ");
      Serial.println(freq);
      break;
    case 0x04:
      Serial.println("read position: ");
      Serial.println(position); 
      break;
    case 0x05:
      Serial.println("stop");
      ctrl_mode=0;
      target_pos=position;
      break;
    case 0x06:
      Serial.println("position reset");
      target_pos=0;
      position=0;
      break;
    default:
      Serial.println("error cmd type");
      break;
  }
}

/*
  serialEvent是一种在接收到串口数据时自动调用的函数，它可以让你在loop()函数执行完后处理串口数据。
  serialEvent会在每次loop()函数结束时被检查，如果串口缓冲区中有可用的数据，就会触发serialEvent。
  你可以使用Serial.read()等函数来读取串口数据，并进行相应的操作。
  如果你的板子有多个串口，你也可以使用serialEvent1()，serialEvent2()等函数来分别处理不同的串口数据。
*/
void serialEvent(){
  static int buf_index=0, end_flag=0;
  static uint8_t buf[10];
  while(Serial.available()>0)
  {
    uint8_t data=Serial.read();
    buf[buf_index++]=data;

    //结束标识符 0x41 0x49(星野爱呜呜呜)
    if(end_flag == 0)
    {
      if(data == 0x41)
      {
        end_flag=1;
      }
    }
    else if(end_flag == 1)
    {
      if(data == 0x49)
      {
        end_flag=0;
        buf_index=0;
        //Serial.println("received data");
        buf_process(buf);
      }
      else {
        end_flag=0;
        buf_index=0;
        Serial.println("error data");
      }
    }

    if(buf_index > 9)
    {
      end_flag=0;
      buf_index=0;
      Serial.println("buf overflow");
    }

  }

}
