from car.hardware.config import (SERVO_STEP, SERVO_EFFECTIVE_ANGLE, SERVO_ZERO_POS)
from car.hardware.pca9685 import Pca9685
from utility.singleton import Singleton


class Servo(Pca9685, metaclass=Singleton):
    def __init__(self):
        super().__init__(SERVO_ZERO_POS)
        self._step = SERVO_STEP

    @property
    def angle(self):
        """
        This property return the car servo current angle
        :return: the servo ange ex:20
        """
        return self._current_angle
