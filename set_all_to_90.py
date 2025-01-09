import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()

# Check if pigpio is connected
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Pin assignments for your servos
servo_pins = {
    "Hip Left": 23,
    "Hip Right": 27,
    "Knee Left": 22,
    "Knee Right": 17
}

def set_servo_angle(pin, angle):
    # Calculate pulse width for the angle (500 to 2500 microseconds)
    pulsewidth = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pin, pulsewidth)

def slow_test_servo(pin, servo_name):
    print(f"Testing {servo_name} slowly...")

    # Move the servo from 0 to 180 degrees slowly
    for angle in range(0, 181, 5):  # Step by 5 degrees for smoother movement
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)  # Slow movement with longer delay

    # Move the servo back from 180 to 0 degrees slowly
    for angle in range(180, -1, -5):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)

    # Print the max angle for the servo
    print(f"{servo_name} max angle reached: 180 degrees")

def fast_test_servo(pin, servo_name):
    print(f"Testing {servo_name} quickly...")

    # Move the servo from 0 to 180 degrees quickly
    for angle in range(0, 181, 10):  # Step by 10 degrees for faster movement
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.05)  # Faster movement with shorter delay

    # Move the servo back from 180 to 0 degrees quickly
    for angle in range(180, -1, -10):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.05)

    # Print the max angle for the servo
    print(f"{servo_name} max angle reached: 180 degrees")

def set_all_to_90():
    print("Setting all servos to 90 degrees...")
    for servo, pin in servo_pins.items():
        set_servo_angle(pin, 90)
    print("All servos set to 90 degrees.")

try:
    # Slow test: Test each servo by moving it from 0 to max angle and back
    for servo, pin in servo_pins.items():
        slow_test_servo(pin, servo)
    
    # Fast test: Test each servo by moving it from 0 to max angle and back quickly
    for servo, pin in servo_pins.items():
        fast_test_servo(pin, servo)

    # After testing, set all servos back to 90 degrees
    set_all_to_90()

finally:
    # Turn off the servos
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)  # Stop PWM signal to the servos
    
    pi.stop()  # Disconnect from pigpio
    print("pigpio cleanup complete.")
