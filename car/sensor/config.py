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
us_config = Config(name='ultrasonic', class_name='UltrasonicFrame', inputs=us_inputs, outputs=us_outputs,
                   is_active=True, is_threaded=True,
                   parameters=['status'])

# Picam Configuration

picam_inputs = None
picam_outputs = {'output_name': 'image_frame', 'output_type': 'sarray'}
picam_config = Config(name='camera', class_name='PiCamera', inputs=picam_inputs, outputs=picam_outputs,
                      is_active=True, is_threaded=True,
                      parameters=['car', 'status', 'driving_nn'])

# Package Configuration
sensor_modules = {us_config.name: us_config,picam_config.name: picam_config}
sensor_config = Config(name='Sensor', modules=sensor_modules)
