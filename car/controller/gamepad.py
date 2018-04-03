# @GamePad setting:
#     btn_x activate agent
#     btn_y activate trainer
#     btn_a breaks
#     btn_b start recording
#     btn_tr inc speed
#     btn_tl dec speed
import threading

from evdev._ecodes import EV_KEY, EV_ABS, BTN_A, BTN_B, BTN_X, BTN_Y, BTN_TR, BTN_TL

from car.hardware.config import ABS_Yaxis, ABs_Xaxis
from car.hardware.f710 import F710
from pilot.trainer.trainer_session import *
from utility.singleton import Singleton


class Gamepad(F710, threading.Thread, metaclass=Singleton):

    def __init__(self, objects):
        F710.__init__(self)
        threading.Thread.__init__(self)
        self.car = objects.get('car')
        self.__abs_Yaxis_up = 0
        self.__abs_Yaxis_down = 0

    def categorize(self, event):
        if event.type == EV_KEY:
            if event.value == 1:
                return
            if event.code == BTN_A:
                self.car.brake()
                store_command('brake')
                print("brake")
            elif event.code == BTN_B:
                if self.car.status.is_recording:
                    self.car.status.stop_recording()
                    print("stop recording")
                    return
                self.car.status.start_recording()
                print("start recording")
            elif event.code == BTN_X:
                # Start threads from car.start_threads()
                if self.car.status.is_agent:
                    return
                self.car.status.activate_agent()
                #self.car.start_threads()
                print("activate agent")
            elif event.code == BTN_Y:
                # Start threads from car.start_threads()
                if self.car.status.is_trainer:
                    return
                self.car.status.activate_trainer()
                #self.car.start_threads()
                print("activate trainer")
            elif event.code == BTN_TR:
                self.car.inc_speed()
                print("BTN_TR")
            elif event.code == BTN_TL:
                self.car.dec_speed()
                print("pause recording")

        elif event.type == EV_ABS:
            if event.value < 0:
                if event.code in ABS_Yaxis:
                    self.__abs_Yaxis_up += 1
                    if self.__abs_Yaxis_up > 5:
                        self.car.move_forward()
                        self.__abs_Yaxis_up = 0
                        store_command('forward')
                        print("go forward")
                elif event.code in ABs_Xaxis:
                    self.car.turn_left()
                    store_command('left')
                    print("go left")

            elif event.value > 0:
                if event.code in ABS_Yaxis:
                    self.__abs_Yaxis_down += 1
                    if self.__abs_Yaxis_down > 5:
                        self.car.move_backward()
                        store_command('backward')
                        print("go backward")
                elif event.code in ABs_Xaxis:
                    self.car.turn_right()
                    store_command('right')
                    print("go right")

    def run(self):
        for event in self.f710.read_loop():
            self.categorize(event)
