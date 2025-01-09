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
    "hip left": 23,
    "knee left": 22,
    "hip right": 27,
    "knee right": 17,
    "left toe": 16,
    "right toe": 26,
}

# Default servo positions (starting at 90 degrees)
servo_positions = {joint: 90 for joint in servo_pins}

# Function to set servo position
def set_servo_angle(pin, angle, reverse=False):
    """
    Sets the servo to a specific angle.
    If `reverse` is True, the angle is flipped (180 - angle).
    """
    if reverse:
        angle = 180 - angle

    # Convert angle to pulsewidth and ensure it is within the valid range (500 to 2500)
    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))  # Ensure pulsewidth stays within range
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Save servo positions to a JSON file
def save_positions(filename="servo_positions.json"):
    with open(filename, "w") as file:
        json.dump(servo_positions, file)
    print(f"Servo positions saved to {filename}.")

# Load servo positions from a JSON file
def load_positions(filename="servo_positions.json"):
    global servo_positions
    try:
        with open(filename, "r") as file:
            servo_positions = json.load(file)
        print(f"Servo positions loaded from {filename}.")
    except FileNotFoundError:
        print(f"No saved positions found in {filename}. Starting with default positions.")

# Main program for manual control
try:
    print("Manual Servo Control Program")
    print("Commands:")
    print("  'set [joint] [angle]' - Set a specific joint to a degree (e.g., 'set Knee Left 120').")
    print("  'show' - Display the current servo positions.")
    print("  'save' - Save the current servo positions.")
    print("  'exit' - Quit the program.")

    # Load saved positions if available
    load_positions()

    # Move servos to their last saved positions
    for joint, angle in servo_positions.items():
        set_servo_angle(servo_pins[joint], angle)

    while True:
        user_input = input("Enter command: ").strip().lower()

        if user_input == "exit":
            break

        elif user_input == "show":
            for joint, angle in servo_positions.items():
                print(f"{joint.title()}: {angle}°")

        elif user_input.startswith("set"):
            try:
                parts = user_input.split()
                joint = " ".join(parts[1:-1])  # Combine middle parts for joint name
                angle = int(parts[-1])
                if joint in servo_pins:
                    servo_positions[joint] = angle
                    reverse = joint in ["right toe"]  # Reverse for oppositely oriented servos
                    set_servo_angle(servo_pins[joint], angle, reverse)
                    print(f"{joint.title()} set to {angle}°")
                else:
                    print(f"Unknown joint: {joint}")
            except (ValueError, IndexError):
                print("Invalid command format. Use: set [joint] [angle]")

        elif user_input == "save":
            save_positions()

        else:
            print("Invalid command. Try 'set', 'show', 'save', or 'exit'.")
finally:
    # Cleanup: Turn off all servos
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
