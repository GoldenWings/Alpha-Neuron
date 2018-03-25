from car.hardware.config import SERVO_STEP
from car.hardware.pca9685 import Pca9685
from utility.singleton import Singleton


class Servo(metaclass=Singleton, Pca9685):
    def __init__(self):
        super().__init__()
        self.step = SERVO_STEP

    def go_right(self):
        self.set_angle((self.current_angle + self.step))

    def go_left(self):
        self.set_angle((self.current_angle - self.step))
