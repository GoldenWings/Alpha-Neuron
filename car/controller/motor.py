from car.hardware.config import MOTOR_SPEED, BREAKS
from car.hardware.md10c import Md10c


class Motor(Md10c):

    def __init__(self):
        super().__init__()

    def run_motor(self):
        self.set_speed(MOTOR_SPEED)

    def stop_motor(self):
        self.set_speed(BREAKS)
