"""

"""

from controller import config as controller
from sensor import config as sensor
from pilot import car as car
from pilot import config as pilot
import sys
import inspect

# Load Configuration

controller_config = controller.controller_config
sensor_config = sensor.sensor_config
pilot_config = pilot.pilot_config


# Initialize objects
"""
We can initialize objects from each active module based on configuration files
"""
objects = [] # List of all objects
# Initialize car Object
for name, obj in inspect.getmembers(sys.modules[controller.__name__]):
        if inspect.isclass(obj) and controller_config.modules['name'] == name:
            objects.append(obj)
