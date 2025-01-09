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
}

# Function to set servo position
def set_servo_angle(pin, angle):
    if angle > 160:
        print(f"Angle limited to 160° for safety on pin {pin}.")
        angle = 160
    pulsewidth = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Crouching Motion Simulation
def crouching_motion(pins):
    print("Simulating crouching motion...")

    # Movement sequences for crouching
    # Each tuple is (angle, delay in seconds)
    movements = [
        # Step 1: Lower hips and bend knees slightly
        {"Hip Left": 100, "Knee Left": 130, "Hip Right": 100, "Knee Right": 130, "Left Toe": 90, "delay": 1.0},
        # Step 2: Bend knees more and press toe down
        {"Hip Left": 120, "Knee Left": 150, "Hip Right": 120, "Knee Right": 150, "Left Toe": 70, "delay": 1.0},
        # Step 3: Return to neutral
        {"Hip Left": 90, "Knee Left": 90, "Hip Right": 90, "Knee Right": 90, "Left Toe": 90, "delay": 1.0},
    ]

    for step in movements:
        for joint, angle in step.items():
            if joint != "delay":
                set_servo_angle(pins[joint], angle)
                print(f"{joint} at {angle}°")
        time.sleep(step["delay"])
    print("Crouching motion simulation complete.")

# Main Program
try:
    print("Control the robot servos for crouching.")
    print("Options:")
    print("  - Type 'crouch' to simulate a crouching motion.")
    print("  - Type 'exit' to quit.")

    while True:
        user_input = input("Enter command: ").strip().lower()
        if user_input == "exit":
            break
        elif user_input == "crouch":
            crouching_motion(servo_pins)
        else:
            print("Invalid command. Try 'crouch' or 'exit'.")

finally:
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
