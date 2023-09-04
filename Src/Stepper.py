"""
This a library to control a stepper motor when more than one motor is used.
As a result, the controller need a serial port, but don't need to init and read it.

author: Leonaruic
GitHub: github.com/semitia
date: 2023-09-04
version: 0.0.1
"""
import serial


def add_tail(cmd):
    # 在指令后面添加0x41 0x49作为帧尾
    cmd.extend([0x41, 0x49])
    return cmd


class StepperCtrl:
    STEP_DISTANCE = 0.001                                           # 单步距离/m

    def __init__(self, port, baud, num):
        self.num = num                                              # 电机编号
        self.speed = 0                                              # 电机速度
        self.ser = serial.Serial(port, baud)
        print("Init StepperCtrl Complete!")

    def set_speed(self, direction, speed):
        # 生成0x01类型的指令
        freq = int(speed / self.STEP_DISTANCE)                                # 将speed转换为频率
        cmd = bytearray([self.num, 0x01, direction, freq >> 8, freq & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def set_position(self, target_position):
        # 生成0x02类型的指令
        cmd = bytearray([self.num, 0x02, target_position >> 8, target_position & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def read_speed(self):
        # 生成0x03类型的指令
        cmd = bytearray([self.num, 0x03])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def read_position(self):
        # 生成0x04类型的指令
        cmd = bytearray([self.num, 0x04])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def stop(self):
        # 生成0x05类型的指令
        cmd = bytearray([self.num, 0x05])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def position_reset(self):
        # 生成0x06类型的指令
        cmd = bytearray([self.num, 0x06])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

