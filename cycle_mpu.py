import pigpio
import smbus
import time
import math
import random

# ==========================
# Hardware Setup
# ==========================
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

servo_pins = {
    "Hip Left": 23,
    "Knee Left": 22,
    "Hip Right": 27,
    "Knee Right": 17,
    "Left Toe": 16,
    "Right Toe": 26,
}

# I2C and MPU6050
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
bus = smbus.SMBus(1)  # I2C bus 1 on Raspberry Pi

def init_mpu():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

init_mpu()

# ==========================
# Functions
# ==========================
def set_servo_angle(pin, angle, reverse=False):
    if reverse:
        angle = 180 - angle
    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))
    pi.set_servo_pulsewidth(pin, pulsewidth)

def move_all_servos(angles):
    for joint, angle in angles.items():
        reverse = joint in ["Right Toe"]
        set_servo_angle(servo_pins[joint], angle, reverse)
    time.sleep(0.1)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value

def read_mpu_data():
    ax = read_raw_data(ACCEL_XOUT_H)
    ay = read_raw_data(ACCEL_XOUT_H + 2)
    az = read_raw_data(ACCEL_XOUT_H + 4)

    ax_g = ax/16384.0
    ay_g = ay/16384.0
    az_g = az/16384.0

    pitch = math.degrees(math.atan2(ax_g, math.sqrt(ay_g*ay_g + az_g*az_g)))
    roll = math.degrees(math.atan2(ay_g, az_g))
    return pitch, roll

def measure_stability(samples=10):
    pitch_sum = 0
    roll_sum = 0
    for _ in range(samples):
        pitch, roll = read_mpu_data()
        pitch_sum += abs(pitch)
        roll_sum += abs(roll)
        time.sleep(0.05)
    avg_pitch_dev = pitch_sum / samples
    avg_roll_dev = roll_sum / samples
    return avg_pitch_dev, avg_roll_dev

def clamp_angle(angle):
    return max(0, min(180, angle))

# ==========================
# Adaptive Small Movements
# ==========================

# Start from a given natural standing position
base_position = {
    "Hip Left": 90,
    "Knee Left": 120,
    "Hip Right": 90,
    "Knee Right": 60,
    "Left Toe": 110,
    "Right Toe": 110
}

move_all_servos(base_position)
time.sleep(1)

# A small movement pattern (like shifting weight)
# We'll try a simple pattern: 
# Phase 1: Slight shift forward (Hip angles decreased slightly)
# Phase 2: Slight shift backward (Hip angles increased slightly)
# Phase 3: Slight shift left (Adjust knees/toes)
# Phase 4: Slight shift right
#
# Over iterations, we tweak these phases to find a more stable pattern.
movement_pattern = [
    {"Hip Left": base_position["Hip Left"] - 5, "Knee Left": base_position["Knee Left"],
     "Hip Right": base_position["Hip Right"] - 5, "Knee Right": base_position["Knee Right"],
     "Left Toe": base_position["Left Toe"], "Right Toe": base_position["Right Toe"]},
     
    {"Hip Left": base_position["Hip Left"] + 5, "Knee Left": base_position["Knee Left"],
     "Hip Right": base_position["Hip Right"] + 5, "Knee Right": base_position["Knee Right"],
     "Left Toe": base_position["Left Toe"], "Right Toe": base_position["Right Toe"]},
     
    {"Hip Left": base_position["Hip Left"], "Knee Left": base_position["Knee Left"] + 5,
     "Hip Right": base_position["Hip Right"], "Knee Right": base_position["Knee Right"],
     "Left Toe": base_position["Left Toe"], "Right Toe": base_position["Right Toe"] - 5},
     
    {"Hip Left": base_position["Hip Left"], "Knee Left": base_position["Knee Left"] - 5,
     "Hip Right": base_position["Hip Right"], "Knee Right": base_position["Knee Right"],
     "Left Toe": base_position["Left Toe"] + 5, "Right Toe": base_position["Right Toe"]}
]

def execute_pattern(pattern):
    for step in pattern:
        move_all_servos(step)
        time.sleep(0.5)
    # Return to base at the end
    move_all_servos(base_position)
    time.sleep(0.5)

# Measure initial stability
best_pattern = [step.copy() for step in movement_pattern]
best_pitch_dev, best_roll_dev = measure_stability()
best_score = best_pitch_dev + best_roll_dev
print(f"Initial stability score: {best_score:.2f}")

ITERATIONS = 10
THRESHOLD_IMPROVEMENT = 0.5
ADJUST_STEP = 2

for i in range(ITERATIONS):
    print(f"Iteration {i+1}...")
    # Execute current best pattern
    execute_pattern(best_pattern)
    # Measure stability
    c_pitch_dev, c_roll_dev = measure_stability()
    candidate_score = c_pitch_dev + c_roll_dev
    print(f"Candidate score: {candidate_score:.2f}")

    # If not stable enough, try adjusting pattern based on pitch/roll
    # Simple heuristic: if leaning forward/back use hips, left/right use knees/toes
    pitch, roll = read_mpu_data()
    candidate_pattern = [step.copy() for step in best_pattern]

    # Adjust steps slightly based on pitch/roll
    # If pitch > 0 (forward), reduce forward hip movement and increase backward movement
    for step_index, step in enumerate(candidate_pattern):
        # If pitch > 0: leaning forward, so reduce steps that push forward hips
        # If pitch < 0: leaning backward, so adjust steps that push backward hips
        pitch_correction = int(-pitch / 10)
        roll_correction = int(-roll / 10)

        # For forward/back steps (0 and 1 in pattern)
        if step_index == 0:  # forward shift
            step["Hip Left"] = clamp_angle(step["Hip Left"] + pitch_correction)
            step["Hip Right"] = clamp_angle(step["Hip Right"] + pitch_correction)
        elif step_index == 1:  # backward shift
            step["Hip Left"] = clamp_angle(step["Hip Left"] + pitch_correction)
            step["Hip Right"] = clamp_angle(step["Hip Right"] + pitch_correction)
        
        # For left/right shifts (2 and 3 in pattern)
        if step_index == 2: # left shift
            step["Knee Left"] = clamp_angle(step["Knee Left"] + roll_correction)
            step["Left Toe"] = clamp_angle(step["Left Toe"] - roll_correction)
        elif step_index == 3: # right shift
            step["Knee Right"] = clamp_angle(step["Knee Right"] - roll_correction)
            step["Right Toe"] = clamp_angle(step["Right Toe"] + roll_correction)

    # Test the candidate pattern
    execute_pattern(candidate_pattern)
    c_pitch_dev2, c_roll_dev2 = measure_stability()
    candidate_score2 = c_pitch_dev2 + c_roll_dev2
    print(f"Adjusted candidate score: {candidate_score2:.2f}")

    # Decide if improved
    if candidate_score2 < best_score - THRESHOLD_IMPROVEMENT:
        best_pattern = candidate_pattern
        best_score = candidate_score2
        print("Found improved pattern!")
    else:
        print("No improvement, keeping previous pattern.")

# Return to base
move_all_servos(base_position)
time.sleep(1)

print(f"Final best score: {best_score:.2f}")

# Cleanup
for pin in servo_pins.values():
    pi.set_servo_pulsewidth(pin, 0)
pi.stop()
print("Cleanup complete, servos off.")
