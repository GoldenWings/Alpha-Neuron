"""
Define a generic interface for  each pilot module

Usage:
    Defines a constant configuration for any added pilot
    with the following constrains:
    Threaded, Inputs, Outputs, is the module currently in use? (Active)
"""

from utility.config import Config

# Trainer
trainer_inputs = None
trainer_outputs = [
    {'output_name': 'session_csv', 'output_type': 'csv'}
]
trainer_config = Config(name='TrainerSession', inputs=trainer_inputs, outputs=trainer_outputs, is_active=True, is_threaded=False)

# Agent
agent_inputs = [
    {'input_name': 'image_frame', 'input_type': 'sarray'}
]
agent_outputs = [
    {'output_name': 'movement_dir', 'output_type': 'integer'}, {'output_name': 'direction', 'output_type': 'integer'}
]
agent_config = Config(name='DrivingNeuralNetwork', inputs=agent_inputs, outputs=agent_outputs, is_active=True, is_threaded=True,
                      parameters=['Car'])

# Package Configuration
pilot_modules = {trainer_config.name: trainer_config, agent_config.name: agent_config}
pilot_config = Config(name='Pilot', modules=pilot_modules)
