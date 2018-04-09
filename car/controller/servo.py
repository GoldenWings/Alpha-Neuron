from car.hardware.config import SERVO_STEP
from car.hardware.pca9685 import Pca9685
from utility.singleton import Singleton


class Servo(Pca9685, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.step = SERVO_STEP

    def turn_right(self):
        self.set_angle((self.current_angle + self.step))

    def turn_left(self):
        self.set_angle((self.current_angle - self.step))

    @property
    def angle(self):
        return self.current_angle
