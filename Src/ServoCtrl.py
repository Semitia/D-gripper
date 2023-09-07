"""
This is a library for Bus Servo Controller. (幻尔总线舵机)
The board uses Serial for communication.

Author: Leonaruic
GitHub: github.com/semitia
Date: 2023-08-08
Version: 0.0.1
"""
import time
import serial
import threading


def checksum(buf):
    # 左闭右开
    temp = sum(buf[2:buf[3] + 2])
    return ~temp & 0xff


class Servo:
    def __init__(self):
        self.temp = 25
        self.pos = 0
        self.vin = 0

class ServoCtrl:
    SERVO_FRAME_HEADER = 0x55
    SERVO_MOVE_TIME_WRITE = 1
    SERVO_MOVE_TIME_READ = 2
    SERVO_MOVE_TIME_WAIT_WRITE = 7
    SERVO_MOVE_TIME_WAIT_READ = 8
    SERVO_MOVE_START = 11
    SERVO_MOVE_STOP = 12
    SERVO_ID_WRITE = 13
    SERVO_ID_READ = 14
    SERVO_ANGLE_OFFSET_ADJUST = 17
    SERVO_ANGLE_OFFSET_WRITE = 18
    SERVO_ANGLE_OFFSET_READ = 19
    SERVO_ANGLE_LIMIT_WRITE = 20
    SERVO_ANGLE_LIMIT_READ = 21
    SERVO_VIN_LIMIT_WRITE = 22
    SERVO_VIN_LIMIT_READ = 23
    SERVO_TEMP_MAX_LIMIT_WRITE = 24
    SERVO_TEMP_MAX_LIMIT_READ = 25
    SERVO_TEMP_READ = 26
    SERVO_VIN_READ = 27
    SERVO_POS_READ = 28
    SERVO_OR_MOTOR_MODE_WRITE = 29
    SERVO_OR_MOTOR_MODE_READ = 30
    SERVO_LOAD_OR_UNLOAD_WRITE = 31
    SERVO_LOAD_OR_UNLOAD_READ = 32
    SERVO_LED_CTRL_WRITE = 33
    SERVO_LED_CTRL_READ = 34
    SERVO_LED_ERROR_WRITE = 35
    SERVO_LED_ERROR_READ = 36

    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)
        self.got_frame_header = False
        self.frame_header_count = 0
        self.data_count = 0
        self.data_length = 2
        self.rx_completed = False
        self.rx_buf = bytearray(15)  # 0,1:header; 2:id; 3:length; 4:cmd; 5~:data; -1:checksum
        self.ReadPortThread = threading.Thread(target=self.read_port)
        self.ReadPortThread.start()
        print("Init ServoCtrl Complete!")

    def read_port(self):
        while True:
            if self.ser.in_waiting > 0:
                msg = self.ser.read(self.ser.in_waiting)
                # print("serial read", msg)
                for byte in msg:
                    self.process_byte(byte)

    def process_byte(self, byte):
        if not self.got_frame_header:
            if byte == 0x55:
                self.frame_header_count += 1
                if self.frame_header_count == 2:
                    self.frame_header_count = 0
                    self.got_frame_header = True
                    self.data_count = 2
                    # print("got frame header!")
            else:
                self.got_frame_header = False
                self.data_count = 0
                self.frame_header_count = 0
                print("frame header error!")
        else:
            self.rx_buf[self.data_count] = byte
            if self.data_count == 3:
                self.data_length = self.rx_buf[self.data_count]
                if self.data_length < 3 or self.data_length > 7:
                    print("data length error!")
                    self.data_length = 3
                    self.got_frame_header = False
            self.data_count += 1
            if self.data_count == self.data_length + 3:
                # print("msg received successfully!")
                self.rx_completed = True
                self.got_frame_header = False

    def set_id(self, old_id, new_id):
        """
        设置Id
        """
        buf = bytearray(7)
        buf[0] = buf[1] = self.SERVO_FRAME_HEADER
        buf[2] = old_id
        buf[3] = 4
        buf[4] = self.SERVO_ID_WRITE
        buf[5] = new_id
        buf[6] = checksum(buf)
        self.ser.write(buf)

    def move(self, servo_id, position, time):
        """
        用一定时间移动到指定位置
        """
        if position < 0:
            position = 0
        if position > 1000:
            position = 1000
        buf = bytearray(10)
        buf[0] = buf[1] = 0x55
        buf[2] = servo_id
        buf[3] = 7
        buf[4] = self.SERVO_MOVE_TIME_WRITE
        buf[5] = position & 0xff
        buf[6] = (position >> 8) & 0xff
        buf[7] = time & 0xff
        buf[8] = (time >> 8) & 0xff
        buf[9] = checksum(buf)
        self.ser.write(buf)

    def unload(self, servo_id):
        """
        卸载舵机
        """
        buf = bytearray(7)
        buf[0] = buf[1] = self.SERVO_FRAME_HEADER
        buf[2] = servo_id
        buf[3] = 4
        buf[4] = self.SERVO_LOAD_OR_UNLOAD_WRITE
        buf[5] = 0
        buf[6] = checksum(buf)
        self.ser.write(buf)

    def load(self, servo_id):
        """
        装载舵机
        """
        buf = bytearray(7)
        buf[0] = buf[1] = self.SERVO_FRAME_HEADER
        buf[2] = servo_id
        buf[3] = 4
        buf[4] = self.SERVO_LOAD_OR_UNLOAD_WRITE
        buf[5] = 1
        buf[6] = checksum(buf)
        self.ser.write(buf)

    def read_response(self):
        count = 50
        while not self.rx_completed:
            count -= 1
            time.sleep(0.001)
            # print("waiting for response")
            if count < 0:
                print("waiting time out")
                return -2048
        # self.ser.in_waiting,属性表示串口接收缓冲区中的字节数
        buf = self.rx_buf
        if checksum(buf) != buf[buf[3] + 2]:
            print("checksum error")
            return -2049
        cmd = buf[4]
        if cmd == self.SERVO_POS_READ:
            ret = buf[6] << 8 | buf[5]
            return ret
        # elif
        return 0

    def read_position(self, servo_id):
        buf = bytearray(6)
        buf[0] = buf[1] = self.SERVO_FRAME_HEADER
        buf[2] = servo_id
        buf[3] = 3
        buf[4] = self.SERVO_POS_READ
        buf[5] = checksum(buf)
        self.ser.write(buf)
        # print("read_position cmd has been send")
        ret = self.read_response()
        print("read_position result: ", ret)
        return ret

    # def update(self):


# controller = ServoCtrl('COM7', 115200)
# controller.read_position(1)
# while True:
#     command = input('Enter a command: \n '
#                     '1. read position <servo_id>\n '
#                     '2. set position <target_position> <target_time> <servo_id>\n')
#     if 'read position' in command or '<1>' in command:
#         # 提取舵机号码
#         target_id = int(command.split()[-1])
#         controller.read_position(target_id)
#         print(f'Reading position of servo {target_id}')
#
#     elif 'set position' in command or '<2>' in command:
#         # 提取目标角度和舵机号码
#         target_position, target_time, target_id = map(int, command.split()[-3:])
#         controller.move(target_id, target_position, target_time)
#         print(f'Setting position of servo {target_id} to {target_position}')
#     else:
#         print('Unknown command')
