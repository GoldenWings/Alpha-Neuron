"""
Define a generic interface for  each controller module

Usage:
    Defines a constant configuration for any added controller
    with the following constrains:
    Threaded, Inputs, Outputs, is the module currently in use? (Active)
"""
from utility.config import Config

# Motor Configuration
motor_inputs = [
    {'input_name': 'movement_dir', 'input_type': 'integer'}
]
motor_outputs = None
motor_config = Config(name='motor', class_name='Motor', inputs=motor_inputs, outputs=motor_outputs, is_active=True,
                      is_threaded=False)

# Servo Configuration
servo_inputs = [
    {'input_name': 'direction', 'input_type': 'integer'}
]
servo_outputs = None
servo_config = Config(name='servo', class_name='Servo', inputs=servo_inputs, outputs=servo_outputs, is_active=True,
                      is_threaded=False)


# Gamepad Configuration
gamepad_inputs = None
gamepad_outputs = [
    {'output_name': 'movement_dir', 'output_type': 'integer'}, {'output_name': 'direction', 'output_type': 'integer'}
]
gamepad_config = Config(name='gamepad', class_name='Gamepad', inputs=gamepad_inputs, outputs=gamepad_outputs,
                        is_active=True,
                        is_threaded=True, parameters=['car'])

# Package Configuration
controller_modules = {motor_config.name: motor_config, servo_config.name: servo_config,
                      gamepad_config.name: gamepad_config}
controller_config = Config(name='Controller', modules=controller_modules)
