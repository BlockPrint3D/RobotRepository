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

# Walking Motion: Moving the legs forward and backward
def walk():
    """
    Perform basic walking by alternating leg movements.
    This will simulate stepping forward.
    """
    print("Starting walk motion...")

    # Define the angles for stepping (moving one leg at a time)
    step_forward_left = {
        "Hip Left": 45,    # Move the left hip forward
        "Knee Left": 130,   # Bend the knee to lift the left leg
        "Left Toe": 130    # Toe angle to lift the left leg
    }
    step_forward_right = {
        "Hip Right": 45,  # Move the right hip forward
        "Knee Right": 50,  # Bend the knee to lift the right leg
        "Right Toe": 130   # Toe angle to lift the right leg
    }
    
    # Define the reset position (natural standing) to bring the lifted leg back down
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
    
    # Move left leg forward and back
    move_all_servos(step_forward_left)
    time.sleep(1)  # Delay for a while to simulate a step
    move_all_servos(reset_position_left)
    time.sleep(1)  # Delay to reset the left leg
    
    # Move right leg forward and back
    move_all_servos(step_forward_right)
    time.sleep(1)  # Delay for a while to simulate a step
    move_all_servos(reset_position_right)
    time.sleep(1)  # Delay to reset the right leg
    
    print("One step completed.")

# Main Program: Perform a basic walking cycle
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
