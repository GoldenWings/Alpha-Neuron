import os

import car.trainer_config as cfg
from utility.singleton import Singleton


class Car(metaclass=Singleton):
    def __init__(self):
        self.__threaded_objects = None
        self.__objects = None
        self.__sensor_objects = None
        self.__is_started = False

    def initialize_objects(self, objects, threaded_objects, sensor_objects):
        self.__threaded_objects = threaded_objects
        self.__objects = {**objects, **threaded_objects}
        self.__sensor_objects = sensor_objects
        self.__objects = {**self.__objects, **self.__sensor_objects}
        self.start_car()

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
        return self.__objects['servo'].angle

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
        return self.__objects['motor'].throttle

    def brake(self):
        self.__objects['motor'].brake()

    def start_car(self, status_is_agent=False):
        if not self.__is_started:
            self.start_sensor()
            self.start_threads()
            self.__is_started = True

    def train(self):
        train_gen, val_gen = self.barrel_reader.generate_training_validation(cfg.BATCH_SIZE,
                                                                             cfg.TRAIN_TEST_SPLIT)
        model_name = 'model_ ' + str(cfg.count_models() + 1)
        model_path = os.path.normpath(model_name)
        model_path = os.path.expanduser(model_path)

        total_records = len(self.barrel_reader.df)
        total_train = int(total_records * cfg.TRAIN_TEST_SPLIT)
        total_val = total_records - total_train

        print('train: %d, validation: %d' % (total_train, total_val))
        steps_per_epoch = total_train // cfg.BATCH_SIZE
        print('steps_per_epoch', steps_per_epoch)

        self.driving_nn.train(train_gen, val_gen, saved_model_path=model_path, steps=steps_per_epoch,
                              train_split=cfg.TRAIN_TEST_SPLIT)

    @property
    def barrel_reader(self):
        return self.__objects['barrel_reader']

    @property
    def driving_nn(self):
        return self.__objects['driving_nn']

    def __del__(self):
        del self.__sensor_objects
        del self.__objects
        del self.__threaded_objects
