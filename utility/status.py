from utility.singleton import Singleton


class Status(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__is_recording = False
        self.__is_agent = False
        self.__is_trainer = False

    @property
    def is_trainer(self):
        return self.__is_trainer

    @property
    def is_agent(self):
        return self.__is_agent
    
    @property
    def is_recording(self):
        return self.__is_recording

    @property
    def sensor_started(self):
        return self.is_agent or self.is_trainer

    def activate_agent(self):
        self.deactivate_trainer()
        self.__is_agent = True

    def activate_trainer(self):
        self.deactivate_agent()
        self.__is_trainer = True

    def deactivate_agent(self):
        self.__is_agent = False

    def deactivate_trainer(self):
        self.__is_trainer = False
        self.stop_recording()

    def start_recording(self):
        self.__is_recording = True

    def stop_recording(self):
        self.__is_recording = False