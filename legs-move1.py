import pigpio
import time

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
    If `reverse` is True, the angle is flipped (180 - angle).
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

# Human-like Walking Motion: Simulate a more fluid walk
def walk():
    """
    Perform a more human-like walking cycle with alternating leg movements,
    smoother transitions, and coordination between hip, knee, and ankle joints.
    """
    print("Starting human-like walk motion...")

    # Define the angles for stepping forward with more fluidity
    step_forward_left = {
        "Hip Left": 60,  # Move the left hip forward to simulate a step
        "Knee Left": 90,  # Bend the knee to simulate lifting the left leg
        "Left Toe": 90    # Lift the left toe slightly
    }
    step_forward_right = {
        "Hip Right": 60,  # Move the right hip forward
        "Knee Right": 90,  # Bend the knee to simulate lifting the right leg
        "Right Toe": 90    # Lift the right toe slightly
    }
    
    # Define reset positions to bring the lifted leg back down after each step
    reset_position_left = {
        "Hip Left": 90,
        "Knee Left": 120,
        "Left Toe": 110
    }
    reset_position_right = {
        "Hip Right": 90,
        "Knee Right": 60,
        "Right Toe": 110
    }

    # Double support phase (both feet on the ground)
    print("Double support phase (both feet on the ground)...")
    move_all_servos(natural_standing_position)
    time.sleep(1)  # Both feet on the ground for stability

    # Move left leg forward and back
    move_all_servos(step_forward_left)
    time.sleep(0.5)  # Half a second to simulate a step forward
    move_all_servos(reset_position_left)
    time.sleep(0.5)  # Delay to reset the left leg
    
    # Move right leg forward and back
    move_all_servos(step_forward_right)
    time.sleep(0.5)  # Half a second to simulate a step forward
    move_all_servos(reset_position_right)
    time.sleep(0.5)  # Delay to reset the right leg
    
    print("Step completed. Switching legs...")

    # Repeat the process for the next cycle
    print("Human-like walk cycle complete.")

# Main Program: Perform a human-like walking cycle
try:
    print("Servo Control Program")
    print("Commands:")
    print("  'walk' - Start walking.")
    print("  'exit' - Quit the program.")
    
    while True:
        user_input = input("Enter command: ").strip().lower()
        
        if user_input == "exit":
            break
        elif user_input == "walk":
            for _ in range(5):  # Walk 5 steps in a loop
                walk()
        else:
            print("Invalid command. Try 'walk' or 'exit'.")
finally:
    # Cleanup: Turn off all servos
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
