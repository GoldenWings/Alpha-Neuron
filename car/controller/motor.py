from car.hardware.config import MOTOR_SPEED, BREAKS
from car.hardware.md10c import Md10c
from utility.singleton import Singleton


class Motor(Md10c, metaclass=Singleton):

    def __init__(self):
        super().__init__()

    def run_motor(self):
        self.set_speed(MOTOR_SPEED)

    def stop_motor(self):
        self.set_speed(BREAKS)
