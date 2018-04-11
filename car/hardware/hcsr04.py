import pigpio

from car.hardware.config import SOUND_SPEED


class Hcsr04:

    def __init__(self, name, pi, trigger, echo):
        self.pi = pi
        self.trig = trigger
        self.name = name

        self._distance = 999.9
        self._one_tick = None

        if trigger is not None:
            pi.set_mode(trigger, pigpio.OUTPUT)

        pi.set_mode(echo, pigpio.INPUT)

        self._cb = pi.callback(echo, pigpio.EITHER_EDGE, self._cbf)

    def _cbf(self, gpio, level, tick):
        """
        This method is to calculate the distance of objects in front of of the sensor using by equation
        distance = velocity * time
        """
        if level == 1:
            self._one_tick = tick
        else:
            if self._one_tick is not None:
                ping_micros = pigpio.tickDiff(self._one_tick, tick)
                self._distance = (ping_micros * SOUND_SPEED) / 2e4
                self._one_tick = None

    def trigger(self):
        """This method is to trigger an echo from the sensor """
        self._distance = 999.9
        self._one_tick = None

        if self.trig is not None:
            self.pi.gpio_trigger(self.trig, 15)  # 15 micros trigger pulse

    def read(self):
        """
        this method return the distance
        :return: it return the distance between the sensor and object in cm ex:15 cm.
        """
        return self._distance

    def cancel(self):
        """this method is used to cancle any on going calculation """
        self._cb.cancel()
