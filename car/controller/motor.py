from car.hardware.config import MOTOR_STEP, BRAKES
from car.hardware.md10c import Md10c
from utility.singleton import Singleton


class Motor(Md10c, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.__current_speed = MOTOR_STEP

    def move_backward(self):
        if self.get_dir():
            self.brake()
            self.set_dir(False)
        self.set_speed(self.__current_speed)

    def move_forward(self):
        if not self.get_dir():
            self.set_dir(True)
        self.set_speed(self.__current_speed)

    def brake(self):
        self.set_speed(BRAKES)

    def inc_speed(self):
        self.__current_speed += MOTOR_STEP
        self.set_speed(self.__current_speed)

    def dec_speed(self):
        self.__current_speed -= MOTOR_STEP
        self.set_speed(self.__current_speed)

    def get_speed(self):
        return self.__current_speed

    def __del__(self):
        super().__del__()
