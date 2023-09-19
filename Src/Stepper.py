"""
This a library to control a stepper motor when more than one motor is used.
As a result, the controller need a serial port, but don't need to init and read it.

author: Leonaruic
GitHub: github.com/semitia
date: 2023-09-04
version: 0.0.1
"""
import time
import serial


def add_tail(cmd):
    # 在指令后面添加0x41 0x49作为帧尾
    cmd.extend([0x41, 0x49])
    return cmd


class StepperCtrl:
    STEP_DISTANCE = 0.001                                           # 单步距离/m

    def __init__(self, num):
        self.num = num                                              # 电机编号
        self.speed = 0                                              # 电机速度
        self.position = 0                                           # 电机位置
        self.speed_updated = False                                  # 电机速度是否更新
        self.pos_updated = False                                    # 电机位置是否更新
        # self.ser = serial.Serial(port, baud)
        print("StepperCtrl ", num, " Init Complete!")

    def set_speed(self, speed, ser):
        # 生成0x01类型的指令
        direction = 0x00
        if speed == 0:
            interval = 0xffff
        else:
            if speed > 0:
                direction = 0x00

            else:
                direction = 0x01
                speed = -speed
            interval = int(1000 * self.STEP_DISTANCE/speed)              # 将speed转换为步进时间间隔

        cmd = bytearray([self.num, 0x01, direction, interval >> 8, interval & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        ser.write(cmd)
        return cmd

    def set_position(self, target_position, ser):
        # 生成0x02类型的指令
        cmd = bytearray([self.num, 0x02, target_position >> 8, target_position & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        ser.write(cmd)
        return cmd

    def read_speed(self, ser):
        # ID，0x03
        cmd = bytearray([self.num, 0x03])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        ser.write(cmd)
        count = 50
        while not self.speed_updated:
            count -= 1
            time.sleep(0.001)
            if count <= 0:
                print("read speed timeout")
                return
        self.speed_updated = False
        print("read successfully")
        return self.speed

    def speed_update(self, speed):
        """
        更新电机速度,同时将speed_updated置为True
        :param speed:
        :return:
        """
        self.speed = speed
        self.speed_updated = True

    def read_position(self, ser):
        # 生成0x04类型的指令
        cmd = bytearray([self.num, 0x04])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        ser.write(cmd)
        count = 50
        while not self.pos_updated:
            count -= 1
            time.sleep(0.001)
            if count <= 0:
                print("read position timeout")
                return
        self.pos_updated = False
        print("read position successfully")

    def pos_update(self, position):
        """
        更新电机位置,同时将pos_updated置为True
        :param position:
        :return:
        """
        self.position = position
        self.pos_updated = True

    def stop(self):
        # 生成0x05类型的指令
        cmd = bytearray([self.num, 0x05])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        # self.ser.write(cmd)
        return cmd

    def position_reset(self):
        # 生成0x06类型的指令
        cmd = bytearray([self.num, 0x06])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        # self.ser.write(cmd)
        return cmd
