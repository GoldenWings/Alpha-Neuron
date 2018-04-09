from car.hardware.config import MOTOR_STEP, MOTOR_MIN_SPEED, MOTOR_MAX_SPEED, BRAKES
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
            self.__current_speed = MOTOR_MIN_SPEED
            self.set_speed(self.__current_speed)
        else:
            return
        self.set_speed(self.__current_speed)

    def move_forward(self):
        if not self.get_dir():
            self.brake()
            self.set_dir(True)
            self.__current_speed = MOTOR_MIN_SPEED
            self.set_speed(self.__current_speed)
        else:
            return
        self.set_speed(self.__current_speed)

    def brake(self):
        self.set_speed(BRAKES)

    def inc_speed(self):
        if (self.__current_speed + MOTOR_STEP) > MOTOR_MAX_SPEED:
            print("The maximum speed reached")
            return
        self.__current_speed += MOTOR_STEP
        self.set_speed(self.__current_speed)

    def dec_speed(self):
        if (self.__current_speed - MOTOR_STEP) < MOTOR_MIN_SPEED:
            print("The minimum speed reached")
            return
        self.__current_speed -= MOTOR_STEP
        self.set_speed(self.__current_speed)

    @property
    def throttle(self):
        return self.__current_speed

    def __del__(self):
        super().__del__()
