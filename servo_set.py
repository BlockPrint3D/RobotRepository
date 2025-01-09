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

# Function to set servo position to 90 degrees
def set_servo_angle(pin, angle):
    """
    Sets the servo to a specific angle (90 degrees in this case).
    """
    if angle != 90:
        print("Setting all servos to 90 degrees.")
        angle = 90  # Always set to 90 degrees

    # Convert angle to pulsewidth and ensure it is within the valid range (500 to 2500)
    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))  # Ensure pulsewidth stays within range
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Set all servos to 90 degrees
def set_all_servos_to_90():
    for pin in servo_pins.values():
        set_servo_angle(pin, 90)
    print("All servos are now set to 90 degrees.")

# Main Program
try:
    print("Setting all servos to 90 degrees...")
    set_all_servos_to_90()
    
    # Keep the servos at 90 degrees until user decides to exit
    print("Servos are now frozen at 90 degrees. Press Ctrl+C to exit.")
    
    # Wait indefinitely while keeping the servos at 90
    while True:
        time.sleep(1)  # Sleep to avoid high CPU usage in the loop
except KeyboardInterrupt:
    # Handle user exit with Ctrl+C
    print("Exiting program.")
finally:
    # Cleanup: Turn off all servos when exiting
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")
