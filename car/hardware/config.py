"""
This file will contain the configuration need for the hardware parts to work

"""
# Motor speed
MOTOR_SPEED = 0.75
BREAKS = 0

# Md10c
MD10C_DIR_PIN = 7
MD10C_PWM_PIN = 12
MD10C_FREQ = 20000

# servo
SERVO_CHANEL = 0
SERVO_MIN_PULSE = 150  # Min pulse length out of 4096
SERVO_MAX_PULSE = 600  # Max pulse length out of 4096
SERVO_STEP = 11.25
SERVO_MAX_ANGLE = 45
SERVO_MIN_ANGLE = -45
SERVO_ZERO_POS = 0

# Hcsr04
SOUND_SPEED = 343
PIN_DIST_TRIG = 40
PIN_DIST_ECHO = 38
PIN_DIST_ECHO2 = 37
PIN_DIST_ECHO3 = 36
PIN_DIST_ECHO4 = 35
PIN_DIST_ECHO5 = 33
