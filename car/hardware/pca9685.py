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

    def _set_angle(self, channel, delta=170):
        """
        This method take the channel that servo is connected to in pca9685 board to send to it the
        pulse the represent the required angle
        :return: it has no return type
        """
        # delay = max(delta * 0.02, 0.02)
        zero_pulse = (self.servo_min + self.servo_max) / 2
        pulse_width = zero_pulse - self.servo_min
        pulse = zero_pulse + (pulse_width * self.current_angle / 80)
        self.pwm.set_pwm(channel, 0, int(pulse))
        # time.sleep(delay)

    def set_angle(self, req_angle):
        """
        This method take the angel that needed to be set to the servo to set it
        :param req_angle: the angle that needed to be set
        :return: it has no return type
        """
        if req_angle <= self.min:
            req_angle = self.min
        elif req_angle >= self.max:
            req_angle = self.max
        self.current_angle = req_angle
        self._set_angle(SERVO_CHANEL)

    def get_angle(self):
        """
        This method return the servo angle
        :return: servo angle ex:20
        """
        return self.current_angle
