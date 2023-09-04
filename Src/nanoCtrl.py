"""
This is a serial controller for Arduino nano board, which is equipped with 3 Stepper Motors and 3 Angle Sensors.
It works with the Stepperx3.ino.

author: Leonaruic
GitHub: github.com/semitia
date: 2023-09-04
version: 0.0.1
"""
import Stepper
import serial
import threading


def add_tail(cmd):
    # 在指令后面添加0x41 0x49作为帧尾
    cmd.extend([0x41, 0x49])
    return cmd


class NanoCtrl:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)
        self.motor[3] = [Stepper(port, baud, i) for i in range(3)]      # 3个电机
        self.ReadPortThread = threading.Thread(target=self.read_port)
        self.ReadPortThread.start()
        print("Init StepperCtrl Complete!")

    def read_port(self):
        while True:
            if self.ser.in_waiting > 0:
                msg = self.ser.read(self.ser.in_waiting)
                # print("serial read", msg.decode())
                for byte in msg:
                    self.process_byte(byte)

    def process_byte(self, byte):
        # 读取到的byte是int类型
        return

    def set_speed(self, direction, freq):
        # 生成0x01类型的指令
        cmd = bytearray([0x01, direction, freq >> 8, freq & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def set_position(self, target_pos):
        # 生成0x02类型的指令
        cmd = bytearray([0x02, target_pos >> 8, target_pos & 0xFF])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def read_speed(self):
        # 生成0x03类型的指令
        cmd = bytearray([0x03])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def read_position(self):
        # 生成0x04类型的指令
        cmd = bytearray([0x04])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def stop(self):
        # 生成0x05类型的指令
        cmd = bytearray([0x05])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)

    def position_reset(self):
        # 生成0x06类型的指令
        cmd = bytearray([0x06])
        # 添加帧尾
        cmd = add_tail(cmd)
        # 发送指令
        self.ser.write(cmd)


controller = NanoCtrl('COM4', 115200)
while True:
    command = input('Enter a command: \n '
                    '1. read position \n '
                    '2. set position <target_position> \n'
                    '3. set speed <direction> <freq> \n'
                    '4. read speed \n'
                    '5. stop \n'
                    '6. position reset \n')
    if 'read position' in command or '<1>' in command:
        controller.read_position()
    elif 'set position' in command or '<2>' in command:
        target_pos = int(command.split(' ')[-1])
        controller.set_position(target_pos)
    elif 'set speed' in command or '<3>' in command:
        direction = int(command.split(' ')[-2])
        freq = int(command.split(' ')[-1])
        controller.set_speed(direction, freq)
    elif 'read speed' in command or '<4>' in command:
        controller.read_speed()
    elif 'stop' in command or '<5>' in command:
        controller.stop()
    elif 'position reset' in command or '<6>' in command:
        controller.position_reset()
    else:
        print('Unknown command')