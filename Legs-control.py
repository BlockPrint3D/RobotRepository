import pigpio
import tkinter as tk
from tkinter import ttk
import time

# Initialize pigpio
pi = pigpio.pi()

# Check if pigpio is connected
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Pin assignments
servo_pins = {
    "Hip Left": 23,
    "Knee Left": 22,
    "Hip Right": 27,
    "Knee Right": 17,  # Installed in the opposite orientation
    "Left Toe": 16,    # New servo pin
}

# Servo control function
def set_servo_angle(pin, angle):
    pulsewidth = 500 + (angle / 180.0) * 2000
    pi.set_servo_pulsewidth(pin, pulsewidth)

# GUI Class
class ServoControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Control Test")
        self.servo_values = {}
        self.create_widgets()

    def create_widgets(self):
        for i, (servo, pin) in enumerate(servo_pins.items()):
            frame = ttk.Frame(self.root)
            frame.grid(row=i, column=0, pady=5, padx=10, sticky="w")

            label = ttk.Label(frame, text=f"{servo} (GPIO {pin}):")
            label.grid(row=0, column=0, sticky="w")

            slider = ttk.Scale(
                frame,
                from_=0,
                to=180,
                orient="horizontal",
                command=lambda value, servo=servo, pin=pin: self.update_servo(pin, int(float(value))),
            )
            slider.set(90)  # Set initial angle to 90 (neutral position)
            slider.grid(row=0, column=1, padx=10)

            self.servo_values[servo] = slider

        # Add a reset button
        reset_button = ttk.Button(self.root, text="Reset All", command=self.reset_all_servos)
        reset_button.grid(row=len(servo_pins), column=0, pady=10)

    def update_servo(self, pin, angle):
        set_servo_angle(pin, angle)

    def reset_all_servos(self):
        for servo, slider in self.servo_values.items():
            slider.set(90)  # Reset all servos to neutral
            pin = servo_pins[servo]
            set_servo_angle(pin, 90)

# Cleanup function to reset all servos
def cleanup():
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    print("pigpio cleanup complete.")

# Run the GUI
try:
    root = tk.Tk()
    app = ServoControlApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (cleanup(), root.destroy()))  # Cleanup on close
    root.mainloop()
finally:
    cleanup()
