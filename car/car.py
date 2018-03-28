from utility.singleton import Singleton


class Car(metaclass=Singleton):
    def __init__(self, objects, threaded_objects):
        self.__threaded_objects = threaded_objects
        self.__objects = {**objects, **threaded_objects}
        self.start_threads()

    @property
    def status(self):
        return self.__objects['Status']

    @property
    def camera(self):
        return self.__objects['Camera']

    @property
    def ultrasonic(self):
        return self.__objects['UltrasonicFrame']

    def start_threads(self):
        for obj in self.__threaded_objects:
            obj.start()

    def turn_right(self):
        self.__objects['Servo'].turn_right()

    def turn_left(self):
        self.__objects['Servo'].turn_left()

    def move_forward(self):
        self.__objects['Motor'].move_forward()

    def move_backward(self):
        self.__objects['Motor'].move_backward()

    def inc_speed(self):
        self.__objects['Motor'].inc_speed()

    def dec_speed(self):
        self.__objects['Motor'].dec_speed()

    def current_speed(self):
        self.__objects['Motor'].get_speed()

    def brake(self):
        self.__objects['Motor'].brake()

    def __del__(self):
        del self.__objects
        del self.__threaded_objects
