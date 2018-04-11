from car.hardware.config import MOTOR_STEP, MOTOR_MIN_SPEED, MOTOR_MAX_SPEED, BRAKES
from car.hardware.md10c import Md10c
from utility.singleton import Singleton


class Motor(Md10c, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self._current_speed = BRAKES

    def move_backward(self):
        """
        This method give the car motor an order to move backward.
        :return: it has no return type.
        """
        if self.get_dir():
            self.brake()
            self.set_dir(False)
            self._current_speed = MOTOR_MIN_SPEED
            self.set_speed(self._current_speed)
        else:
            return
        self.set_speed(self._current_speed)

    def move_forward(self):
        """
        This method give the car motor an order to move forward.
        :return: it has no return type.
        """
        if not self.get_dir():
            self.brake()
            self.set_dir(True)
            self._current_speed = MOTOR_MIN_SPEED
            self.set_speed(self._current_speed)
        else:
            return
        self.set_speed(self._current_speed)

    def brake(self):
        """
        This method used to set the car motor speed to zero (breaks)
        :return: it has no return value
        """
        self.set_speed(BRAKES)

    def inc_speed(self):
        """
        This function is used to increase the car motor speed.
        :return: it has no return type
        """
        if (self._current_speed + MOTOR_STEP) > MOTOR_MAX_SPEED:
            return
        self._current_speed += MOTOR_STEP
        self.set_speed(self._current_speed)

    def dec_speed(self):
        """
        This method is used to decrease the car motor speed.
        :return: it has no return type
        """
        if (self._current_speed - MOTOR_STEP) < MOTOR_MIN_SPEED:
            return
        self._current_speed -= MOTOR_STEP
        self.set_speed(self._current_speed)

    @property
    def throttle(self):
        """
        This function return the motor current speed.
        :return: current speed
        """
        return self._current_speed

    def __del__(self):
        super().__del__()
