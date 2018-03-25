import threading
import time

import pigpio

from car.hardware.hcsr04 import Hcsr04
from utility.frameDic import FrameDict


class UltrasonicFrame(threading.Thread):

    def __init__(self, uprep=None):
        threading.Thread.__init__(self)
        self.pi = pigpio.pi()
        self.S = []
        self.uprep = None
        if uprep is not None:
            self.uprep = uprep
        self.initialize_sonics()
        self.frame = FrameDict(f3=0, f4=0, r=0, b3=0, b2=0, b1=0, l=0, f1=0, f2=0)
        self._start = True

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
        '''
            This function returns a frame and if the Mode is trainer and recording then call
            store_session, if mode is agent then notify agent
        :return: 1 Ultrasonic frame
        '''
        for s in self.S:
            self.frame[s.name] = int(round(s.read(), 0))
        return self.frame

    def run(self):
        self._start = True
        # counter = 0
        while self._start:
            for s in self.S:
                s.trigger()
            time.sleep(0.5)
            self.get_frame()

    def stop(self):
        self._start = False
        for s in self.S:
            s.cancel()
        self.pi.stop()
