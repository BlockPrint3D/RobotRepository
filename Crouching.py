import pigpio
import time
import smbus
import math

# Initialize pigpio
pi = pigpio.pi()

# Check if pigpio is connected
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Pin assignments for servos
servo_pins = {
    "Hip Left": 23,
    "Knee Left": 22,
    "Hip Right": 27,
    "Knee Right": 17,
    "Left Toe": 16,
    "Right Toe": 26,
}

# Natural standing position
natural_standing_position = {
    "Hip Left": 90,
    "Knee Left": 120,
    "Hip Right": 90,
    "Knee Right": 60,
    "Left Toe": 110,
    "Right Toe": 110,
}

# MPU6050 setup
MPU6050_ADDR = 0x68
bus = smbus.SMBus(1)  # Use I2C bus 1

def initialize_mpu6050():
    bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)  # Wake up the MPU6050

initialize_mpu6050()

# Function to read raw data from MPU6050
def read_mpu6050_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value

# Function to get tilt angles from MPU6050
def get_tilt_angles():
    accel_x = read_mpu6050_raw_data(0x3B)
    accel_y = read_mpu6050_raw_data(0x3D)
    accel_z = read_mpu6050_raw_data(0x3F)

    pitch = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2)) * 180 / math.pi
    roll = math.atan2(accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi

    return pitch, roll

# Function to set servo position
def set_servo_angle(pin, angle, reverse=False):
    if reverse:
        angle = 180 - angle

    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Move all servos simultaneously
def move_all_servos(angles):
    for joint, angle in angles.items():
        reverse = joint in ["Right Toe"]
        set_servo_angle(servo_pins[joint], angle, reverse)
        print(f"{joint} moved to {angle}°")

# Adjust servos to maintain balance
def balance_robot():
    pitch, roll = get_tilt_angles()
    print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}")

    adjustment = {
        "Hip Left": natural_standing_position["Hip Left"] + roll,
        "Knee Left": natural_standing_position["Knee Left"] - pitch,
        "Hip Right": natural_standing_position["Hip Right"] - roll,
        "Knee Right": natural_standing_position["Knee Right"] + pitch,
        "Left Toe": natural_standing_position["Left Toe"],
        "Right Toe": natural_standing_position["Right Toe"],
    }

    move_all_servos(adjustment)

# Main loop
try:
    print("Balancing Robot Program")
    while True:
        balance_robot()
        time.sleep(0.1)  # Small delay for feedback loop

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
