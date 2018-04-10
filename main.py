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

# Load Configuration

utility_config = utility.utility_config
controller_config = controller.controller_config
sensor_config = sensor.sensor_config
pilot_config = pilot.pilot_config


# Initialize objects
"""
We can initialize objects from each active module based on configuration files
"""
# Initialize non parameterized objects
"""
First Initialize non parameterized objects, and add parameterized objects into dictionary for later Initialization
"""
non_tp_objects = {}  # Dictionary of non threaded non parameterized objects
non_p_objects = {}  # Dictionary of threaded non parameterized objects
parameterized_objects = {}  # Dictionary of all parameterized objects
sensor_objects = {}
car = Car()
non_p_objects['car'] = car

# Initialize utility module objects
for name, obj in inspect.getmembers(sys.modules['utility']):
        if inspect.isclass(obj) and name in utility_config.modules and utility_config.modules[name].is_active:
            print(name)
            if utility_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, utility_config.modules[name].parameters,
                                               utility_config.modules[name].threaded]
            else:
                if utility_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  # Initialize object and append to non threaded non parameterized
        elif name in utility_config.modules and inspect.ismodule(obj) and utility_config.modules[name].is_active:
            print(name)
            obj = getattr(obj, utility_config.modules[name].class_name)
            if utility_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, utility_config.modules[name].parameters,
                                               utility_config.modules[name].threaded]
            else:
                if utility_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  # Initialize object and append to non threaded non parameterized

# Initialize controller module objects
for name, obj in inspect.getmembers(sys.modules['car.controller']):
        if inspect.isclass(obj) and name in controller_config.modules and controller_config.modules[name].is_active:
            if controller_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, controller_config.modules[name].parameters,
                                               controller_config.modules[name].threaded]
            else:
                if controller_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  # Initialize object and append to non threaded non parameterized
        elif name in controller_config.modules and inspect.ismodule(obj) and controller_config.modules[name].is_active:
            obj = getattr(obj, controller_config.modules[name].class_name)
            if controller_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, controller_config.modules[name].parameters,
                                               controller_config.modules[name].threaded]
            else:
                if controller_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  #

# Initialize sensor module objects
for name, obj in inspect.getmembers(sys.modules['car.sensor']):
        if inspect.isclass(obj) and name in sensor_config.modules and sensor_config.modules[name].is_active:
            if sensor_config.modules[name].parameterized:
                # append to parameterized objects list for later Initialization
                parameterized_objects[name] = [obj, sensor_config.modules[name].parameters,
                                               sensor_config.modules[name].threaded]
            else:
                if sensor_config.modules[name].threaded:
                    non_p_objects[name] = obj()
                else:
                    non_tp_objects[name] = obj()  # Initialize object and append
        elif name in sensor_config.modules and inspect.ismodule(obj) and sensor_config.modules[name].is_active:
            obj = getattr(obj, sensor_config.modules[name].class_name)
            if sensor_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, sensor_config.modules[name].parameters,
                                               sensor_config.modules[name].threaded]
            else:
                if sensor_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  #

# Initialize pilot module objects
for name, obj in inspect.getmembers(sys.modules['pilot.agent']):
        if inspect.isclass(obj) and name in pilot_config.modules and pilot_config.modules[name].is_active:
            if pilot_config.modules[name].parameterized:
                # append to parameterized objects list for later Initialization
                parameterized_objects[name] = [obj, pilot_config.modules[name].parameters,
                                               pilot_config.modules[name].threaded]
            else:
                if pilot_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  # Initialize object and append to non threaded non parameterized
        elif name in pilot_config.modules and inspect.ismodule(obj) and pilot_config.modules[name].is_active:
            obj = getattr(obj, pilot_config.modules[name].class_name)
            if pilot_config.modules[name].parameterized:
                # append to parameterized objects dictionary for later Initialization
                parameterized_objects[name] = [obj, pilot_config.modules[name].parameters,
                                               pilot_config.modules[name].threaded]
            else:
                if pilot_config.modules[name].threaded:
                    non_p_objects[name] = obj()  # Initialize object and append to threaded non parameterized
                else:
                    non_tp_objects[name] = obj()  #

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


def get_parameters(parameterized_object):
    p_param = {}  # dictionary of parameters to be passed to the object
    for param in parameterized_object[1]:
        if param in non_tp_objects:
            p_param[param] = non_tp_objects[param]
        elif param in non_p_objects:
            p_param[param] = non_p_objects[param]
        elif param in parameterized_objects:
            p_object = parameterized_objects.pop(param)  # Remove it from parameterized_objects dictionary and return it
            p_object[0] = p_object[0](get_parameters(p_object))
            p_param[param] = p_object[0]
            if p_object[2]:  # if threaded add to threaded non parameterized dictionary
                non_p_objects[param] = p_object[0]
            else:
                non_tp_objects[param] = p_object
    return p_param


for key in list(parameterized_objects):
    # [key] will return array, [0] will return the un-initialized object
    # After it return the un-initialized object it will initialize it using the parameters from get_parameters
    if key not in parameterized_objects:
        continue
    obj = parameterized_objects[key][0](get_parameters(parameterized_objects[key]))
    if parameterized_objects[key][2]:
        non_p_objects[key] = obj
    else:
        non_tp_objects[key] = obj
    del parameterized_objects[key]


# Separate sensor objects
for k in list(non_p_objects):
    if k in sensor_config.modules:
        sensor_objects[k] = non_p_objects[k]
        del non_p_objects[k]

# Initialize car object
car.initialize_objects(non_tp_objects, non_p_objects, sensor_objects)
