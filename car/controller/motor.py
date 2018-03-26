from car.hardware.config import MOTOR_SPEED, BRAKES
from car.hardware.md10c import Md10c
from utility.singleton import Singleton


class Motor(Md10c, metaclass=Singleton):

    def __init__(self):
        super().__init__()

    def move_backward(self):
        if self.get_dir():
            self.brake()
            self.set_dir(False)
        self.set_speed(MOTOR_SPEED)

    def move_forward(self):
        if not self.get_dir():
            self.set_dir(True)
        self.set_speed(MOTOR_SPEED)

    def brake(self):
        self.set_speed(BRAKES)

    def __del__(self):
        super().__del__()
