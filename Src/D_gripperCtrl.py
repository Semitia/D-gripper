"""

"""

from ServoCtrl import ServoCtrl
from nanoCtrl import NanoCtrl
import keyboard
import time


class DgripperCtrl:
    def __init__(self, servo_port, servo_baud, nano_port, nano_baud):
        self.Servo = ServoCtrl(servo_port, servo_baud)
        self.nano = NanoCtrl(nano_port, nano_baud)
        print("Init DgripperCtrl Complete!")

    def __init__(self):
        print("Init DgripperCtrl Complete!")

    def run(self):
        while True:
            if keyboard.is_pressed('q'):
                # 夹爪1张开
                self.Servo.move(1, 1000, 1000)
            elif keyboard.is_pressed('w'):
                # 夹爪2张开
                self.Servo.move(2, 1000, 1000)
            elif keyboard.is_pressed('e'):
                # 夹爪3张开
                self.Servo.move(3, 1000, 1000)
            elif keyboard.is_pressed('u'):



            self.Servo.update()
            time.sleep(0.1)


no1 = DgripperCtrl()
no1.run()





