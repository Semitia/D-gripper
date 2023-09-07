"""
This is a library for an Angle sensor, whose feedback is an analog signal.
The range of the analog signal is 0~5V (if its voltage supply is 5V), corresponding to -160~160 degree.
We acquire the analog signal by Arduino nano's ADC, and then send it to the PC by serial.
"""


class AngleSensor:
    def __init__(self):
        self.angle = 0
        self.angle_offset = 0
        self.angle_raw = 0
        self.vol = 0

    def set_angle_offset(self, angle_offset):
        self.angle_offset = angle_offset

    def update(self, voltage):
        self.vol = voltage
        self.angle_raw = (voltage - 2.5) * 160 / 2.5
        self.angle = self.angle_raw - self.angle_offset
        return self.angle

    def get_angle(self):
        return self.angle

