from car.hardware.config import (SERVO_STEP, SERVO_EFFECTIVE_ANGLE, SERVO_ZERO_POS)
from car.hardware.pca9685 import Pca9685
from utility.singleton import Singleton


class Servo(Pca9685, metaclass=Singleton):
    def __init__(self):
        self._current_angle = SERVO_ZERO_POS
        super().__init__(self._current_angle)
        self._step = SERVO_STEP

    def turn_right(self):
        """This method turn the car servo angel to the right by value of step."""
        if (self._current_angle + self._step) in range(SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1]):
            self.set_angle((self._current_angle + self._step))
            self._current_angle += self._step

    def turn_left(self):
        """This method turn the car servo angel to the left by value of step."""
        if (self._current_angle - self._step) in range(SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1]):
            self.set_angle((self._current_angle - self._step))
            self._current_angle -= self._step

    @property
    def angle(self):
        """
        This property return the car servo current angle
        :return: the servo ange ex:20
        """
        return self.current_angle
