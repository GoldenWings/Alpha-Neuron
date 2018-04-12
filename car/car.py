import os

import car.trainer_config as cfg
from utility.singleton import Singleton


class Car(metaclass=Singleton):
    def __init__(self):
        self._threaded_objects = None
        self._objects = None
        self._sensor_objects = None
        self._is_started = False

    def initialize_objects(self, objects, threaded_objects, sensor_objects):
        """this method take list of needed object from all package config file and start initiating it """
        self._threaded_objects = threaded_objects
        self._objects = {**objects, **threaded_objects}
        self._sensor_objects = sensor_objects
        self._objects = {**self._objects, **self._sensor_objects}
        self.start_car()

    @property
    def status(self):
        """
        This method return the obj that represent the car status
        :return: a Status obj
        """
        return self._objects['status']

    @property
    def camera(self):
        """
        This method return the obj that represent the car camera
        :return: Camera obj
        """
        return self._objects['camera']

    @property
    def ultrasonic(self):
        """
        This method return the obj that represent the car ultrasonic
        :return: UltrasonicFrame obj
        """
        return self._objects['ultrasonic']

    def start_sensor(self):
        """This method start the car sensors that is in _sensor_objects """
        for o in self._sensor_objects.values():
            o.start()

    def start_threads(self):
        """This method start the car threaded obj that is in _threaded_objects """
        for obj in self._threaded_objects.values():
            if obj is self:
                continue
            obj.start()

    def turn_right(self):
        """This method turn the car right """
        self._objects['servo'].turn_right()

    def turn_left(self):
        """This method turn the car left """
        self._objects['servo'].turn_left()

    def set_angle(self, req_angle):
        self._objects['servo'].set_angle(req_angle)

    @property
    def current_angle(self):
        """
        This method return the car servo current angle
        :return: current angle ex:20
        """
        return self._objects['servo'].angle

    def move_forward(self):
        """This method move the car forward """
        self._objects['motor'].move_forward()

    def move_backward(self):
        """This method move the car backward"""
        self._objects['motor'].move_backward()

    def inc_speed(self):
        """This method increase the car speed """
        self._objects['motor'].inc_speed()

    def dec_speed(self):
        """This method decrease the car speed """
        self._objects['motor'].dec_speed()

    @property
    def current_speed(self):
        """
        This method return the car current speed
        :return: speed ex:0.50
        """
        return self._objects['motor'].throttle

    def brake(self):
        """This method is used to stop the car or by other mean this is the breaks """
        self._objects['motor'].brake()

    def start_car(self, status_is_agent=False):
        """This is the method that start the car by starting the car sensors and threads """
        if not self._is_started:
            self.start_sensor()
            self.start_threads()
            self._is_started = True
        if status_is_agent:
            self.start_threads()

    def train(self):
        """
            This method is responsible for reading (latest or a given data barrel)
            then it split the data into training and validation sets according to batch size and split rate
            Then loads a model and fit it with the generated data set.
            Finally store it to disk for later use.
         """
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

        x = self.driving_nn.train(train_gen, val_gen, saved_model_path=model_path, steps=steps_per_epoch,
                              train_split=cfg.TRAIN_TEST_SPLIT)
        print(x)

    @property
    def barrel_reader(self):
        """
        This method is used to return the barrel, that used in data saving process
        :return: barrel obj
        """
        return self._objects['barrelreader']

    @property
    def driving_nn(self):
        """
        This method return a driving__nn obj that is used to predict an angle and throttle according the data stream
        :return: driving_nn obj
        """
        return self._objects['driving_nn']

    def __del__(self):
        del self._sensor_objects
        del self._objects
        del self._threaded_objects
