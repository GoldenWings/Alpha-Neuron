import RPi.GPIO as GPIO

from car.hardware.config import MD10C_DIR_PIN, MD10C_FREQ, MD10C_PWM_PIN
from utility.singleton import Singleton


class Md10c(metaclass=Singleton):
    __md10c_dir_pin = MD10C_DIR_PIN
    __md10c_pwm_pin = MD10C_PWM_PIN
    __md10c_freq = MD10C_FREQ
    __md10c_dir = 1
    __md10c_speed = 0

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # method to setup mode of pin referring scheme
        GPIO.setwarnings(False)  # set warning mode off
        GPIO.setup(self.__md10c_dir_pin, GPIO.OUT)  # setup md10c_dir to be output pin
        GPIO.setup(self.__md10c_pwm_pin, GPIO.OUT)  # setup md10c_pwm to be output pin
        GPIO.output(self.__md10c_dir_pin, GPIO.HIGH)  # setup md10c_dir to have HIGH signal of 1
        self.p = GPIO.PWM(self.__md10c_pwm_pin, 1)  # initiate object from class PWM to handle pwm operation
        self.p.start(0)  # set the duty cycle by zero

    def set_dir(self, direction):
        if direction is 1:
            GPIO.output(self.__md10c_dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.__md10c_dir_pin, GPIO.LOW)

    def set_speed(self, requested_speed):
        """
                :param requested_speed: the speed required by the motor ranged from 0 to 1
                if requested speed is 0, that means the request is break
                It sets the speed to slow down in higher speeds, waits .01 second change frequency and duty to
                full stop.
        """
        self.__md10c_speed = requested_speed
        if requested_speed == 0:
            self.p.ChangeFrequency(1)
            self.p.ChangeDutyCycle(0)
            return
        else:
            speed = (float(self.__md10c_freq) * float(requested_speed))  # calculate the speed required in Hz
            self.p.ChangeFrequency(speed)  # changing the frequency of pulse to the frequency of required speed
            self.p.ChangeDutyCycle(100 * requested_speed)  # setup the required duty cycle for the required speed)
