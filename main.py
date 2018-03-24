"""
Usage: Loads configuration and acts as starting point of the project
"""

import inspect
import sys

from car.controller import config as controller
from car.sensor import config as sensor
from pilot import config as pilot

# Load Configuration

controller_config = controller.controller_config
sensor_config = sensor.sensor_config
pilot_config = pilot.pilot_config


# Initialize objects
"""
We can initialize objects from each active module based on configuration files
"""
objects = {}  # List of all objects
# Initialize car Object
for name, obj in inspect.getmembers(sys.modules[controller.__name__]):
        if inspect.isclass(obj) and name in controller_config.modules and controller_config.modules['name'].is_active:
            objects[name] = obj()  # Initialize object and append
