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
        if level == 1:
            self._one_tick = tick
        else:
            if self._one_tick is not None:
                ping_micros = pigpio.tickDiff(self._one_tick, tick)
                self._distance = (ping_micros * SOUND_SPEED) / 2e4
                self._one_tick = None

    def trigger(self):
        self._distance = 999.9
        self._one_tick = None

        if self.trig is not None:
            self.pi.gpio_trigger(self.trig, 15)  # 15 micros trigger pulse

    def read(self):
        return self._distance

    def cancel(self):
        self._cb.cancel()
