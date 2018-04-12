import Adafruit_PCA9685

from car.hardware.config import (SERVO_MIN_PULSE, SERVO_MAX_PULSE, SERVO_MAX_ANGLE,
                                 SERVO_MIN_ANGLE, SERVO_CHANEL)


class Pca9685:
    def __init__(self, starting_angle):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pulse_min = SERVO_MIN_PULSE
        self.pulse_max = SERVO_MAX_PULSE
        self.angle_max = SERVO_MAX_ANGLE
        self.angle_min = SERVO_MIN_ANGLE
        self.set_angle(starting_angle)
        self.pwm.set_pwm_freq(60)

    def set_angle(self, req_angle, channel=SERVO_CHANEL):
        """
        This method take the channel that servo is connected to in pca9685 board to send to it the
        pulse the represent the required angle using the equation
        req_angle_pulse = ((Angle_max - Angle_min) / (Pulse_max - Pulse_min)) * (req_angle - Pulse_max) + Angle_max
        but at first you need to calibrate the servo config ex max_angle max_pulse,etc... in config.py file in hardware
        package.
        :return: it has no return type
        """
        req_angle_pulse = ((self.angle_max - self.angle_min) / (self.pulse_max - self.pulse_min)) * (
                req_angle - self.pulse_max) + self.angle_max
        self.pwm.set_pwm(channel, 0, int(req_angle_pulse))
