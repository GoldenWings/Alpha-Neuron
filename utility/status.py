from utility.singleton import Singleton


class Status(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._is_recording = False
        self._is_agent = False
        self._is_trainer = True
        self._is_paused = False

    @property
    def is_trainer(self):
        return self._is_trainer

    @property
    def is_agent(self):
        return self._is_agent
    
    @property
    def is_recording(self):
        return self._is_recording

    @property
    def is_paused(self):
        return self._is_paused

    @property
    def sensor_started(self):
        return self.is_agent or self.is_trainer

    def activate_agent(self):
        self.deactivate_trainer()
        self._is_agent = True

    def activate_trainer(self):
        self.deactivate_agent()
        self._is_trainer = True

    def deactivate_agent(self):
        self._is_agent = False

    def deactivate_trainer(self):
        self._is_trainer = False
        self.stop_recording()

    def start_recording(self):
        self._is_recording = True

    def pause_recording(self):
        self._is_recording = False
        self._is_paused = True

    def continue_recording(self):
        self._is_paused = False
        self._is_recording = True

    def stop_recording(self):
        self._is_recording = False

    def reset_recording_status(self):
        self._is_recording = False
        self._is_paused = False
