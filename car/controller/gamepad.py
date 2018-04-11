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
        self.logger = objects.get('logger')
        self._abs_Yaxis_up = 0
        self._abs_Yaxis_down = 0
        self._abs_Xaxis_right = 0
        self._abs_Xaxis_left = 0
        self._start_time = None
        self._end_time = None

    def categorize(self, event):
        """
        This function take an event to categorize it, and do whatever that event represent.
        :param event: is a evdev event.
        :return: it has no return value
        """
        if event.type == EV_KEY:
            if event.value == 0:
                return
            if event.code == BTN_A:
                self.car.brake()
                self.logger.log("brake")
            elif event.code == BTN_B:
                if self.car.status.is_agent:
                    self.logger.log("Agent mode has no recording state")
                else:
                    if self.car.status.is_recording:
                        self.car.status.pause_recording()
                        self.logger.log("Pause recording")
                    else:
                        self.logger.log("There is no recording to pause")
            elif event.code == BTN_X:
                if self.car.status.is_agent:
                    self.logger.log("The agent is already activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.logger.log("Unable to change the mode there is on going training session")
                    else:
                        self.car.status.activate_agent()
                        self.car.start_car(True)
                        self.logger.log("Activate agent")
            elif event.code == BTN_Y:
                if self.car.status.is_trainer:
                    self.logger.log('The trainer mode is already activated')
                else:
                    self.car.status.activate_trainer()
                    self.logger.log('Activate trainer')
            elif event.code == BTN_TR:
                if self.car.status.is_trainer:
                    self.car.inc_speed()
                    self.logger.log('Increase speed')
                else:
                    self.logger.log("Can't inc speed on agent mode")
            elif event.code == BTN_TL:
                if self.car.status.is_trainer:
                    self.car.dec_speed()
                    self.logger.log("Decrease speed")
                else:
                    self.logger.log("Can't dec speed on agent mode")
            elif event.code == BTN_START:
                # logitech start BTN
                if self.car.status.is_agent:
                    self.logger.log("Unable to start recording, the car is on agent mode")
                else:
                    if self.car.status.is_trainer:
                        if self.car.status.is_paused:
                            self.car.status.continue_recording()
                            self.logger.log('Continue recording')
                        else:
                            self._start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            self.car.status.start_recording()
                            self.logger.log('Start recording')
            elif event.code == BTN_MODE:
                # logitech main BTN
                if self.car.status.is_agent:
                    self.logger.log("No session to abort, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.logger.log("Start aborting the session it may take some time")
                        self.car.status.reset_recording_status()
                        self._end_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        self.barrel_writer.abort_csv(self._start_time, self._end_time)
                        self.logger.log("The session has been aborted successfully")
                    else:
                        self.logger.log("There is no session to abort")
            elif event.code == BTN_SELECT:
                # logitech Back
                if self.car.status.is_agent:
                    self.logger.log("No session to save, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.car.status.reset_recording_status()
                        self.barrel_writer.save_csv(self._start_time)
                        self.logger.log('Save session ')
                    else:
                        self.logger.log("There is no session to save")
        elif event.type == EV_ABS and self.car.status.is_trainer:

            if event.value < 0:
                if event.code in ABS_Yaxis:
                    self._abs_Yaxis_up += 1
                    if self._abs_Yaxis_up > 5:
                        self.car.move_forward()
                        self._abs_Yaxis_up = 0
                        self.logger.log("Go forward")
                elif event.code in ABs_Xaxis:
                    self._abs_Xaxis_left += 1
                    if self._abs_Xaxis_left > 2:
                        self.car.turn_left()
                        self._abs_Xaxis_left = 0
                        if self._abs_Xaxis_right < 3:
                            self._abs_Xaxis_right = 0
                        self.logger.log("Go left")

            elif event.value > 0:
                if event.code in ABS_Yaxis:
                    self._abs_Yaxis_down += 1
                    if self._abs_Yaxis_down > 5:
                        self.car.move_backward()
                        self._abs_Yaxis_down = 0
                        self.logger.log("Go backward")
                elif event.code in ABs_Xaxis:
                    self._abs_Xaxis_right += 1
                    if self._abs_Xaxis_right > 2:
                        self.car.turn_right()
                        self._abs_Xaxis_right = 0
                        if self._abs_Xaxis_left < 3:
                            self._abs_Xaxis_left = 0
                        self.logger.log("Go right")

    def start(self):
        if not self.is_alive():
            super().start()

    def run(self):
        for event in self.f710.read_loop():
            self.categorize(event)
