from utility.singleton import Singleton


class Car(metaclass=Singleton):
    def __init__(self):
        self.__threaded_objects = None
        self.__objects = None
        self.__sensor_objects = None

    def initialize_objects(self, objects, threaded_objects, sensor_objects):
        self.__threaded_objects = threaded_objects
        self.__objects = {**objects, **threaded_objects}
        self.__sensor_objects = sensor_objects
        self.__objects = {**self.__objects, **self.__sensor_objects}
        self.start_threads()

    @property
    def status(self):
        return self.__objects['status']

    @property
    def camera(self):
        return self.__objects['camera']

    @property
    def ultrasonic(self):
        return self.__objects['ultrasonic']

    def start_sensor(self):
        for o in self.__sensor_objects.values():
            o.start()

    def start_threads(self):
        for obj in self.__threaded_objects.values():
            if obj is self:
                continue
            obj.start()

    def turn_right(self):
        self.__objects['servo'].turn_right()

    def turn_left(self):
        self.__objects['servo'].turn_left()

    @property
    def current_angle(self):
        return self.__objects['servo'].get_angle()

    def move_forward(self):
        self.__objects['motor'].move_forward()

    def move_backward(self):
        self.__objects['motor'].move_backward()

    def inc_speed(self):
        self.__objects['motor'].inc_speed()

    def dec_speed(self):
        self.__objects['motor'].dec_speed()

    @property
    def current_speed(self):
        return self.__objects['motor'].get_speed()

    def brake(self):
        self.__objects['motor'].brake()

    def __del__(self):
        del self.__objects
        del self.__threaded_objects
