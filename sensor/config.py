"""
Define a generic interface for  each sensor module

Usage:
    Defines a constant configuration for any added sensor
    with the following constrains:
    Threaded, Inputs, Outputs
"""
from utility.config import Config

# Ultrasonic Configuration
us_inputs = None
us_outputs = [
    {'output_name': 'us_frame', 'output_type': 'FrameDict'}
]
us_config = Config(name='Ultrasonic', inputs=us_inputs, outputs=us_outputs, is_active=True, is_threaded=True)

# Picam Configuration

picam_inputs = None
picam_outputs = {'output_name': 'image_frame', 'output_type': 'sarray'}
picam_config = Config(name='PiCam', inputs=picam_inputs, outputs=picam_outputs, is_active=True, is_threaded=True)

# Package Configuration
sensor_modules = [us_config, picam_config]
sensor_config = Config(name='Sensor', modules=sensor_modules)
