import pigpio

# Initialize pigpio
pi = pigpio.pi()

# Check if pigpio is connected
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Pin assignments for each servo
servo_pins = {
    "Hip Left": 23,
    "Knee Left": 22,
    "Hip Right": 27,
    "Knee Right": 17,
}

# Function to set servo position
def set_servo_angle(pin, angle):
    pulsewidth = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pin, pulsewidth)

# Function to release the servo
def release_servo(pin):
    pi.set_servo_pulsewidth(pin, 0)

# Interactive script
try:
    while True:
        # Display servo options
        print("\nSelect a servo to control:")
        for i, servo in enumerate(servo_pins.keys(), start=1):
            print(f"{i}. {servo}")

        print("5. Exit")

        # Get user input
        choice = input("Enter the number of your choice: ")

        # Handle user input
        if choice == "5":
            print("Exiting...")
            break
        elif choice in [str(i) for i in range(1, 5)]:
            servo_name = list(servo_pins.keys())[int(choice) - 1]
            servo_pin = servo_pins[servo_name]

            print(f"\nWhat would you like to do with {servo_name}?")
            print("1. Set to 90 degrees")
            print("2. Release (stop PWM signal)")

            action = input("Enter the number of your choice: ")

            if action == "1":
                print(f"Setting {servo_name} to 90 degrees...")
                set_servo_angle(servo_pin, 90)
            elif action == "2":
                print(f"Releasing {servo_name}...")
                release_servo(servo_pin)
            else:
                print("Invalid action. Please try again.")
        else:
            print("Invalid choice. Please try again.")

finally:
    # Cleanup: Turn off all servos
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    
    pi.stop()
    print("pigpio cleanup complete.")
