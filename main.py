"""
Usage: Loads configuration and acts as starting point of the project
"""

import inspect
import sys
from car.car import Car
from car.controller import config as controller
from car.sensor import config as sensor
from pilot import config as pilot
from utility import utility_config as utility
from utility.logger import Logger
from utility.singleton import Singleton
import traceback


class Main(metaclass=Singleton):
    logger = Logger()

    def __init__(self):
        # Load Configuration
        self.utility_config = utility.utility_config
        self.controller_config = controller.controller_config
        self.sensor_config = sensor.sensor_config
        self.pilot_config = pilot.pilot_config
        # Initialize objects
        """
        We can initialize objects from each active module based on configuration files
        """
        # Initialize non parameterized objects
        """
        First Initialize non parameterized objects, and add parameterized objects into dictionary 
        for later Initialization
        """
        self.non_tp_objects = {}  # Dictionary of non threaded non parameterized objects
        self.non_p_objects = {}  # Dictionary of threaded non parameterized objects
        self.parameterized_objects = {}  # Dictionary of all parameterized objects
        self.sensor_objects = {}
        self.car = Car()
        self.non_p_objects['car'] = self.car
        self.non_tp_objects['logger'] = Main.logger
        # Initialize utility module objects
        self.initialize_utility()
        # Initialize controller module objects
        self.initialize_controller()
        # Initialize sensor module objects
        self.initialize_sensor()
        # Initialize pilot module objects
        self.initialize_pilot()
        # Initialize parameterized objects
        """
            parameterized_objects structure:
            Type Dictionary => key : value
                Key is the name of objects' class to be initialized.
                Value is array of 3 elements: 
                    Value[0]: un-initialized object
                    Value[1]: List of the name of parameters 
                    Value[2]: is threaded?
        """

        for key in list(self.parameterized_objects):
            # [key] will return array, [0] will return the un-initialized object
            # After it return the un-initialized object it will initialize it using the parameters from get_parameters
            if key not in self.parameterized_objects:
                continue
            obj = self.parameterized_objects[key][0](self.get_parameters(self.parameterized_objects[key]))
            if self.parameterized_objects[key][2]:
                self.non_p_objects[key] = obj
            else:
                self.non_tp_objects[key] = obj
            del self.parameterized_objects[key]

        # Separate sensor objects
        for k in list(self.non_p_objects):
            if k in self.sensor_config.modules:
                self.sensor_objects[k] = self.non_p_objects[k]
                del self.non_p_objects[k]

        # Initialize car object
        self.car.initialize_objects(self.non_tp_objects, self.non_p_objects, self.sensor_objects)

    def initialize_utility(self):
        for name, obj in inspect.getmembers(sys.modules['utility']):
            if inspect.isclass(obj) and name in self.utility_config.modules and \
                    self.utility_config.modules[name].is_active:
                if self.utility_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.utility_config.modules[name].parameters,
                                                        self.utility_config.modules[name].threaded]
                else:
                    if self.utility_config.modules[name].threaded:
                        self.non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                    else:
                        # Initialize object and append to non threaded non parameterized
                        self.non_tp_objects[name] = obj()
            elif name in self.utility_config.modules and inspect.ismodule(obj) \
                    and self.utility_config.modules[name].is_active:
                print(name)
                obj = getattr(obj, self.utility_config.modules[name].class_name)
                if self.utility_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.utility_config.modules[name].parameters,
                                                        self.utility_config.modules[name].threaded]
                else:
                    if self.utility_config.modules[name].threaded:
                        self.non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                    else:
                        # Initialize object and append to non threaded non parameterized
                        self.non_tp_objects[name] = obj()

    def initialize_controller(self):
        for name, obj in inspect.getmembers(sys.modules['car.controller']):
            if inspect.isclass(obj) and name in self.controller_config.modules \
                    and self.controller_config.modules[name].is_active:
                if self.controller_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.controller_config.modules[name].parameters,
                                                        self.controller_config.modules[name].threaded]
                else:
                    if self.controller_config.modules[name].threaded:
                        # Initialize object and append to threaded non parameterized
                        self.non_p_objects[name] = obj()
                    else:
                        # Initialize object and append to non threaded non parameterized
                        self.non_tp_objects[name] = obj()
            elif name in self.controller_config.modules and inspect.ismodule(obj) \
                    and self.controller_config.modules[name].is_active:
                obj = getattr(obj, self.controller_config.modules[name].class_name)
                if self.controller_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.controller_config.modules[name].parameters,
                                                        self.controller_config.modules[name].threaded]
                else:
                    if self.controller_config.modules[name].threaded:
                        # Initialize object and append to threaded non parameterized
                        self.non_p_objects[name] = obj()
                    else:
                        self.non_tp_objects[name] = obj()

    def initialize_sensor(self):
        for name, obj in inspect.getmembers(sys.modules['car.sensor']):
            if inspect.isclass(obj) and name in self.sensor_config.modules \
                    and self.sensor_config.modules[name].is_active:
                if self.sensor_config.modules[name].parameterized:
                    # append to parameterized objects list for later Initialization
                    self.parameterized_objects[name] = [obj, self.sensor_config.modules[name].parameters,
                                                        self.sensor_config.modules[name].threaded]
                else:
                    if self.sensor_config.modules[name].threaded:
                        self.non_p_objects[name] = obj()
                    else:
                        self.non_tp_objects[name] = obj()  # Initialize object and append
            elif name in self.sensor_config.modules and inspect.ismodule(obj) \
                    and self.sensor_config.modules[name].is_active:
                obj = getattr(obj, self.sensor_config.modules[name].class_name)
                if self.sensor_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.sensor_config.modules[name].parameters,
                                                        self.sensor_config.modules[name].threaded]
                else:
                    if self.sensor_config.modules[name].threaded:
                        # Initialize object and append to threaded non parameterized
                        self.non_p_objects[name] = obj()
                    else:
                        self.non_tp_objects[name] = obj()  #

    def initialize_pilot(self):
        for name, obj in inspect.getmembers(sys.modules['pilot.agent']):
            if inspect.isclass(obj) and name in self.pilot_config.modules \
                    and self.pilot_config.modules[name].is_active:
                if self.pilot_config.modules[name].parameterized:
                    # append to parameterized objects list for later Initialization
                    self.parameterized_objects[name] = [obj, self.pilot_config.modules[name].parameters,
                                                        self.pilot_config.modules[name].threaded]
                else:
                    if self.pilot_config.modules[name].threaded:
                        # Initialize object and append to threaded non parameterized
                        self.non_p_objects[name] = obj()
                    else:
                        # Initialize object and append to non threaded non parameterized
                        self.non_tp_objects[name] = obj()
            elif name in self.pilot_config.modules and inspect.ismodule(obj) \
                    and self.pilot_config.modules[name].is_active:
                obj = getattr(obj, self.pilot_config.modules[name].class_name)
                if self.pilot_config.modules[name].parameterized:
                    # append to parameterized objects dictionary for later Initialization
                    self.parameterized_objects[name] = [obj, self.pilot_config.modules[name].parameters,
                                                        self.pilot_config.modules[name].threaded]
                else:
                    if self.pilot_config.modules[name].threaded:
                        # Initialize object and append to threaded non parameterized
                        self.non_p_objects[name] = obj()
                    else:
                        self.non_tp_objects[name] = obj()

    def get_parameters(self, parameterized_object):
        p_param = {}  # dictionary of parameters to be passed to the object
        for param in parameterized_object[1]:
            if param in self.non_tp_objects:
                p_param[param] = self.non_tp_objects[param]
            elif param in self.non_p_objects:
                p_param[param] = self.non_p_objects[param]
            elif param in self.parameterized_objects:
                # Remove it from parameterized_objects dictionary and return it
                p_object = self.parameterized_objects.pop(param)
                p_object[0] = p_object[0](self.get_parameters(p_object))
                p_param[param] = p_object[0]
                if p_object[2]:  # if threaded add to threaded non parameterized dictionary
                    self.non_p_objects[param] = p_object[0]
                else:
                    self.non_tp_objects[param] = p_object
        return p_param


if __name__ == "__main__":
    try:
        main = Main()
        # print('Start')
        # main.car.train()
        # print('Finish')
    except Exception as error:
        trace = traceback.format_exc()
        mssg = '{}\n{}'.format(trace, str(error))
        Main.logger.log(mssg, type(error).__name__)
