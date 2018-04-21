import RPi.GPIO as GPIO

from car.hardware.config import MD10C_DIR_PIN, MD10C_FREQ, MD10C_PWM_PIN
from time import sleep

class Md10c:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # method to setup mode of pin referring scheme
        GPIO.setwarnings(False)  # set warning mode off
        self._md10c_dir_pin = MD10C_DIR_PIN
        self._md10c_pwm_pin = MD10C_PWM_PIN
        self._md10c_freq = MD10C_FREQ
        self._md10c_dir_isforward = True
        self._md10c_speed = 0
        if GPIO.gpio_function(self._md10c_dir_pin) is GPIO.OUT:
            GPIO.cleanup(self._md10c_dir_pin)
        if GPIO.gpio_function(self._md10c_pwm_pin) is GPIO.OUT:
            GPIO.cleanup(self._md10c_pwm_pin)
        GPIO.setup(self._md10c_dir_pin, GPIO.OUT)  # setup md10c_dir to be output pin
        GPIO.setup(self._md10c_pwm_pin, GPIO.OUT)
        GPIO.output(self._md10c_dir_pin, GPIO.HIGH)  # setup md10c_dir to have HIGH signal of 1
        self.p = GPIO.PWM(self._md10c_pwm_pin, 1)  # initiate object from class PWM to handle pwm operation
        self.p.start(0)  # set the duty cycle by zero

    def set_dir(self, isforward=True):
        """
        This method set the motor driver current direction.
        :param isforward: take boolean that represent the direction true is forward false is backward.
        :return: it has no return type
        """
        if isforward is True:
            GPIO.output(self._md10c_dir_pin, GPIO.HIGH)
            self._md10c_dir_isforward = True
        else:
            GPIO.output(self._md10c_dir_pin, GPIO.LOW)
            self._md10c_dir_isforward = False

    def get_dir(self):
        return self._md10c_dir_isforward

    def set_speed(self, requested_speed):
        """
        This method set the frequency and the duty cycle of the motor driver current.
        :param requested_speed:the speed required by the motor ranged from 0 to 1
        if requested speed is 0, that means the request is breakIt sets the speed to slow down in higher speeds,
        waits .01 second change frequency and duty to full stop.
        :return: it has no return type.
        """
        self._md10c_speed = requested_speed
        if requested_speed == 0:
            self.p.ChangeFrequency(1)
            self.p.ChangeDutyCycle(0)
            return
        else:
            speed = (float(self._md10c_freq) * float(requested_speed))  # calculate the speed required in Hz
            self.p.ChangeFrequency(speed)  # changing the frequency of pulse to the frequency of required speed
            self.p.ChangeDutyCycle(100 * requested_speed)  # setup the required duty cycle for the required speed)

    def __del__(self):
        GPIO.cleanup(
            [MD10C_PWM_PIN, MD10C_DIR_PIN])  # cleaning up the channel used by _md10c_dir_pin & _md10c_pwm_pin
        self.p.stop()  # stop the pwm duty cycle
