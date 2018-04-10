# @GamePad setting:
#     btn_x activate agent
#     btn_y activate trainer
#     btn_a breaks
#     btn_b pause recording
#     btn_tr inc speed
#     btn_tl dec speed
#     btn_start start recording
#     btn_back save session
#     btn_logitech abort session
import threading
from datetime import datetime

from evdev._ecodes import EV_KEY, EV_ABS, BTN_A, BTN_B, BTN_X, BTN_Y, BTN_TR, BTN_TL, BTN_START, BTN_SELECT, BTN_MODE

from car.hardware.config import ABS_Yaxis, ABs_Xaxis
from car.hardware.f710 import F710
from utility.singleton import Singleton


class Gamepad(F710, threading.Thread, metaclass=Singleton):

    def __init__(self, objects):
        F710.__init__(self)
        threading.Thread.__init__(self)
        self.car = objects.get('car') 
        self.barrel_writer = objects.get('barrelwriter')
        self.__abs_Yaxis_up = 0
        self.__abs_Yaxis_down = 0
        self.__abs_Xaxis_right = 0
        self.__abs_Xaxis_left = 0
        self.__start_time = None
        self.__end_time = None

    def categorize(self, event):
        if event.type == EV_KEY:
            if event.value == 0:
                return
            if event.code == BTN_A:
                self.car.brake()
                print("brake")
            elif event.code == BTN_B:
                if self.car.status.is_agent:
                    print("Agent mode has no recording state")
                else:
                    if self.car.status.is_recording:
                        self.car.status.pause_recording()
                        self.car.start_car(True)
                        print("pause recording")
                    else:
                        print("there is no recording to pause")
            elif event.code == BTN_X:
                if self.car.status.is_agent:
                    print("The agent is already activated")

                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        print("Unable to change the mode there is on going training session ")
                    else:
                        self.car.status.activate_agent()
                        print("activate agent")
            elif event.code == BTN_Y:
                if self.car.status.is_trainer:
                    print("The trainer mode is already activated")
                else:
                    self.car.status.activate_trainer()
                    print("activate trainer")
            elif event.code == BTN_TR:
                if self.car.status.is_trainer:
                    self.car.inc_speed()
                    print("increase speed")
                else:
                    print("can't inc speed on agent mode")
            elif event.code == BTN_TL:
                if self.car.status.is_trainer:
                    self.car.dec_speed()
                    print("decrease speed")
                else:
                    print("can't dec speed on agent mode")
            elif event.code == BTN_START:
                # logitech start BTN
                if self.car.status.is_agent:
                    print("unable to start recording, the car is on agent mode")
                else:
                    if self.car.status.is_trainer:
                        if self.car.status.is_paused:
                            self.car.status.continue_recording()
                            print('continue recording')
                        else:
                            self.__start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            self.car.status.start_recording()
                            print('start recording')
            elif event.code == BTN_MODE:
                # logitech main BTN
                if self.car.status.is_agent:
                    print("No session to abort, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        print("Start aborting the session it may take some time")
                        self.car.status.reset_recording_status()
                        self.__end_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        self.barrel_writer.abort_csv(self.__start_time, self.__end_time)
                        print("The session has been aborted successfully")
                    else:
                        print("There is no session to abort")
            elif event.code == BTN_SELECT:
                # logitech Back
                if self.car.status.is_agent:
                    print("No session to save, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.car.status.reset_recording_status()
                        self.barrel_writer.save_csv(self.__start_time)
                        print('save session ')
                    else:
                        print("There is no session to save")
        elif event.type == EV_ABS and self.car.status.is_trainer:

            if event.value < 0:
                if event.code in ABS_Yaxis:
                    self.__abs_Yaxis_up += 1
                    if self.__abs_Yaxis_up > 5:
                        self.car.move_forward()
                        self.__abs_Yaxis_up = 0
                        print("go forward")
                elif event.code in ABs_Xaxis:
                    self.__abs_Xaxis_left += 1
                    if self.__abs_Xaxis_left > 2:
                        self.car.turn_left()
                        self.__abs_Xaxis_left = 0
                        if self.__abs_Xaxis_right < 3:
                            self.__abs_Xaxis_right = 0
                        print("go left")

            elif event.value > 0:
                if event.code in ABS_Yaxis:
                    self.__abs_Yaxis_down += 1
                    if self.__abs_Yaxis_down > 5:
                        self.car.move_backward()
                        self.__abs_Yaxis_down = 0
                        print("go backward")
                elif event.code in ABs_Xaxis:
                    self.__abs_Xaxis_right += 1
                    if self.__abs_Xaxis_right > 2:
                        self.car.turn_right()
                        self.__abs_Xaxis_right = 0
                        if self.__abs_Xaxis_left < 3:
                            self.__abs_Xaxis_left = 0
                        print("go right")

    def start(self):
        if not self.is_alive():
            super().start()

    def run(self):
        for event in self.f710.read_loop():
            self.categorize(event)
