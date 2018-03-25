import Adafruit_PCA9685

from car.hardware.config import SERVO_MIN_PULSE, SERVO_MAX_PULSE, SERVO_MAX_ANGLE, SERVO_MIN_ANGLE, SERVO_ZERO_POS, \
    SERVO_CHANEL


class Pca9685:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.servo_min = SERVO_MIN_PULSE
        self.servo_max = SERVO_MAX_PULSE
        self.max = SERVO_MAX_ANGLE
        self.min = SERVO_MIN_ANGLE
        self.zero_pos = SERVO_ZERO_POS
        self.current_angle = self.zero_pos
        self.set_angle(self.zero_pos)
        self.pwm.set_pwm_freq(60)

    def __set_angle(self, channel, delta=170):
        # delay = max(delta * 0.02, 0.02)
        zero_pulse = (self.servo_min + self.servo_max) / 2
        pulse_width = zero_pulse - self.servo_min
        pulse = zero_pulse + (pulse_width * self.current_angle / 80)
        self.pwm.set_pwm(channel, 0, int(pulse))

    def set_angle(self, req_angle):
        if req_angle < self.min:
            req_angle = self.min
        elif req_angle > self.max:
            req_angle = self.servo_max
        self.current_angle = req_angle
        self.__set_angle(SERVO_CHANEL, req_angle)

    def get_angle(self):
        return self.current_angle
