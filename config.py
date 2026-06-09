"""
========================
Fire Fighting Rover
Central Configuration File
========================

Controller  : ESP32 Dev Board
Motor Driver: L298N
Power       : Single 12V battery
"""

# ========================
# CONTROLLER SETTINGS
# ========================
BOARD = "ESP32"
POWER_SUPPLY_VOLTAGE = 12  # Volts


# ========================
# MOTOR DRIVER (L298N)
# ========================
# Motor control pins
MOTOR_IN1 = 26
MOTOR_IN2 = 27
MOTOR_IN3 = 12
MOTOR_IN4 = 13

# PWM enable pins
MOTOR_ENA = 25
MOTOR_ENB = 14

# PWM configuration
MOTOR_PWM_FREQUENCY = 1000  # Hz
MOTOR_PWM_RESOLUTION = 8    # bits (0–255)


# ========================
# ULTRASONIC SENSOR (HC-SR04)
# ========================
ULTRASONIC_TRIG_PIN = 5
ULTRASONIC_ECHO_PIN = 18

# Distance thresholds (cm)
STOP_DISTANCE_CM = 20
ULTRASONIC_MAX_RANGE_CM = None  # Not enforced


# ========================
# IR FIRE SENSORS
# ========================
IR_LEFT_PIN = 32
IR_CENTER_PIN = 33
IR_RIGHT_PIN = 35

IR_ACTIVE_STATE = 0  # LOW means fire detected (common for IR flame sensors)


# ========================
# CAMERA & SERVO CONTROL
# ========================
# USB webcam handled by external laptop
VISION_SOURCE = "EXTERNAL_LAPTOP"

# Camera pan servo
CAMERA_SERVO_PIN = 23

# Water nozzle servo
NOZZLE_SERVO_PIN = 19

# Servo angles
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
SERVO_CENTER_ANGLE = 90


# ========================
# WATER PUMP (Relay HW-482)
# ========================
PUMP_RELAY_PIN = 22
PUMP_ACTIVE_STATE = 1  # HIGH activates relay


# ========================
# FIRE ALIGNMENT (VISION)
# ========================
FIRE_ALIGNMENT_TOLERANCE = None  # Vision system decides alignment


# ========================
# SYSTEM TIMING & SAFETY
# ========================
MAIN_LOOP_DELAY_MS = 50          # Stable & responsive
FAILSAFE_STOP_TIMEOUT_SEC = 120  # Stop rover if no fire detected


# ========================
# DEBUG SETTINGS
# ========================
DEBUG_MODE = True
LOG_SENSOR_DATA = True
LOG_DECISIONS = True
