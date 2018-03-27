import threading
import time

import pigpio

from car.hardware.hcsr04 import Hcsr04
from utility.frameDic import FrameDict


class UltrasonicFrame(threading.Thread):

    def __init__(self, objects):
        threading.Thread.__init__(self)
        self.pi = None
        self.S = []
        self.initialize_sensor()
        self.frame = FrameDict(f3=0, f4=0, r=0, b3=0, b2=0, b1=0, l=0, f1=0, f2=0)
        self.status = objects.get('Status')

    def initialize_sensor(self):
        if self.pi is not None:
            self.stop()
        self.pi = pigpio.pi()
        self.initialize_sonics()

    def initialize_sonics(self):
        if not self.pi.connected:
            exit()
        self.S = []
        self.S.append(Hcsr04('f1', self.pi, None, 6))
        self.S.append(Hcsr04('f2', self.pi, None, 13))
        self.S.append(Hcsr04('f3', self.pi, None, 19))
        self.S.append(Hcsr04('f4', self.pi, None, 26))
        self.S.append(Hcsr04('b1', self.pi, None, 16))
        self.S.append(Hcsr04('b2', self.pi, None, 20))
        self.S.append(Hcsr04('b3', self.pi, None, 21))
        self.S.append(Hcsr04('r', self.pi, None, 12))
        self.S.append(Hcsr04('l', self.pi, 9, 5))

    def get_frame(self):
        for s in self.S:
            self.frame[s.name] = int(round(s.read(), 0))
        return self.frame

    def run(self):
        while self.status.sensor_started:
            for s in self.S:
                s.trigger()
            time.sleep(0.5)
            self.get_frame()
        self.stop()

    def stop(self):
        for s in self.S:
            s.cancel()
        self.pi.stop()
