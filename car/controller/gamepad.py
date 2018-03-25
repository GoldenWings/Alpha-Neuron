import threading

from evdev._ecodes import EV_KEY, EV_ABS, BTN_A, BTN_B, BTN_X, BTN_Y, BTN_TR, BTN_TL

from car.hardware.f710 import F710
from utility.singleton import Singleton

ABS_Yaxis = [17, 1]
ABs_Xaxis = [16, 3]


class Gamepad(F710, metaclass=Singleton, threading.Thread):

    def __init__(self):
        super().__init__()

    def __categorize(event):
        if event.type == EV_KEY:
            if event.value == 1:
                pass
            if event.code == BTN_A:
                print("start recording")
            elif event.code == BTN_B:
                print("stop recording")
            elif event.code == BTN_X:
                print("activate agent")
            elif event.code == BTN_Y:
                print("activate_tranier")
            elif event.code == BTN_TR:
                print("BTN_TR")
            elif event.code == BTN_TL:
                print("pause recording")

        elif event.type == EV_ABS:
            if event.value < 0:
                if event.code in ABS_Yaxis:
                    print("go forward")
                elif event.code in ABs_Xaxis:
                    print("go left")

            elif event.value > 0:
                if event.code in ABS_Yaxis:
                    print("go backward")
                elif event.code in ABs_Xaxis:
                    print("go right")
        else:
            pass

    def run(self):
        for event in self.f710.read_loop():
            self.__categorize(event)
