import pigpio
import time
import json

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

# Natural standing position (initial values, can be adjusted)
natural_standing_position = {
    "Hip Left": 90,
    "Knee Left": 120,
    "Hip Right": 90,
    "Knee Right": 60,
    "Left Toe": 110,
    "Right Toe": 110
}

# Function to set servo position
def set_servo_angle(pin, angle, reverse=False):
    """
    Sets the servo to a specific angle.
    If reverse is True, the angle is flipped (180 - angle).
    """
    if reverse:
        angle = 180 - angle

    # Convert angle to pulsewidth and ensure it is within the valid range (500 to 2500)
    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))  # Ensure pulsewidth stays within range
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Move all servos simultaneously by setting them all in one go
def move_all_servos(angles):
    """
    Moves all servos to their respective target angles at the same time.
    """
    for joint, angle in angles.items():
        reverse = joint in ["Right Toe"]  # Reverse for oppositely oriented servos
        set_servo_angle(servo_pins[joint], angle, reverse)
        print(f"{joint} moved to {angle}°")

# Crouching Motion Simulation with 2-second delays
def crouch():
    """
    Perform crouch motion (move toes and knees to crouch position).
    """
    print("Crouching...")

    crouch_angles = {
        "Left Toe": 160, 
        "Right Toe": 160,
        "Knee Left": 180,
        "Knee Right": 0
    }
    
    # Move all servos to crouch position
    move_all_servos(crouch_angles)
    time.sleep(2)  # Delay after crouching

def stand():
    """
    Perform standing motion (move all servos to natural standing position).
    """
    print("Standing...")

    # Move all servos to natural standing position
    move_all_servos(natural_standing_position)
    time.sleep(2)  # Delay after standing

# Main Program: Loop between crouching and standing
try:
    print("Servo Control Program")
    print("Commands:")
    print("  'exit' - Quit the program.")
    
    while True:
        # Perform crouch and stand cycle in a loop
        crouch()
        time.sleep(2)  # Wait before standing
        stand()
        time.sleep(2)  # Wait before crouching again

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    # Cleanup: Turn off all servos
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
