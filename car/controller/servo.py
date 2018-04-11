from car.hardware.config import SERVO_STEP
from car.hardware.pca9685 import Pca9685
from utility.singleton import Singleton


class Servo(Pca9685, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.step = SERVO_STEP

    def turn_right(self):
        """This method turn the car servo angel to the right by value of step."""
        self.set_angle((self.current_angle + self.step))

    def turn_left(self):
        """This method turn the car servo angel to the left by value of step."""
        self.set_angle((self.current_angle - self.step))

    @property
    def angle(self):
        """
        This property return the car servo current angle
        :return: the servo ange ex:45
        """
        return self.current_angle
