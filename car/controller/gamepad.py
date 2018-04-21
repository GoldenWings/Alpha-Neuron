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
from asyncore import file_dispatcher, loop
from evdev._ecodes import (EV_KEY, EV_ABS, BTN_A,
                           BTN_B, BTN_X, BTN_Y, BTN_TR, BTN_TL, BTN_START, BTN_SELECT, BTN_MODE)
from utility.utility import normalize
from car.hardware.config import (ABS_Yaxis, ABs_Xaxis, throttle_min, throttle_max, angle_min, angle_max,
                                 SERVO_EFFECTIVE_ANGLE)
from car.hardware.f710 import F710
from utility.singleton import Singleton


class Gamepad(F710, file_dispatcher, threading.Thread, metaclass=Singleton):

    def __init__(self, objects):
        F710.__init__(self)
        threading.Thread.__init__(self)
        file_dispatcher.__init__(self, self.f710)
        self.car = objects.get('car') 
        self.barrel_writer = objects.get('barrelwriter')
        self.logger = objects.get('logger')
        self._start_time = None

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
                    self.logger.log('Increasing speed {}'.format(self.car.current_speed))
                else:
                    self.logger.log("Can't inc speed on agent mode")
            elif event.code == BTN_TL:
                if self.car.status.is_trainer:
                    self.car.dec_speed()
                    self.logger.log("Decreasing speed {}".format(self.car.current_speed))
                else:
                    self.logger.log("Can't dec speed on agent mode")
            elif event.code == BTN_START:
                # logitech start BTN
                if self.car.status.is_agent:
                    self.logger.log("Unable to start recording, the car is on agent mode")
                else:
                    if self.car.status.is_trainer:
                        if self.car.status.is_recording:
                            self.logger.log("There is an on-going recording in progress!")
                        elif self.car.status.is_paused:
                            self.car.status.continue_recording()
                            self.car.barrel_writer.start_saving()
                            self.logger.log('Continue recording')
                        else:
                            self._start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            self.car.status.start_recording()
                            self.car.barrel_writer.make_session_dir()
                            self.car.barrel_writer.start_saving()
                            self.logger.log('Start recording')
            elif event.code == BTN_MODE:
                # logitech main BTN
                if self.car.status.is_agent:
                    self.logger.log("No session to abort, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.logger.log("Start aborting the session it may take some time")
                        self.car.status.reset_recording_status()
                        self.logger.log("Aborting Session...")
                        self.car.abort_session()
                    else:
                        self.logger.log("There is no session to abort")
            elif event.code == BTN_SELECT:
                # logitech Back
                if self.car.status.is_agent:
                    self.logger.log("No session to save, the agent mode is activated")
                else:
                    if self.car.status.is_recording or self.car.status.is_paused:
                        self.car.status.reset_recording_status()
                        self.logger.log('Session saving started...')
                        self.car.save_session(self._start_time)
                    else:
                        self.logger.log("There is no session to save")
        elif event.type == EV_ABS and self.car.status.is_trainer:

            if event.value < 0:
                if event.code in ABS_Yaxis:
                    throttle = normalize(event.value, -1, 1, throttle_min, throttle_max)
                    self.car.set_throttle(throttle)
                    self.logger.log("Going forward with throttle = " + str(throttle))
                elif event.code in ABs_Xaxis:
                    angle = normalize(event.value, SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1],
                                      angle_min, angle_max)
                    self.logger.log("Going left with angle = {}".format(self.car.current_angle))
                    self.car.set_angle(angle)

            elif event.value > 0:
                if event.code in ABS_Yaxis:
                    throttle = normalize(event.value, -1, 1, throttle_min, throttle_max)
                    self.car.set_throttle(throttle)
                    self.logger.log("Going backward with throttle = " + str(throttle))
                elif event.code in ABs_Xaxis:
                    angle = normalize(event.value, SERVO_EFFECTIVE_ANGLE[0], SERVO_EFFECTIVE_ANGLE[1],
                                      angle_min, angle_max)
                    self.car.set_angle(angle)
                    self.logger.log("Going right with angle = {}".format(self.car.current_angle))

    def recv(self, ign=None):
        return self.f710.read()

    def start(self):
        if not self.is_alive():
            super().start()

    def handle_read(self):
        for event in self.recv():
            self.categorize(event)

    def run(self):
        loop()
