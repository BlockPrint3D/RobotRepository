import pigpio
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading

# ----------------------------
# 1. PIGPIO INITIALIZATION
# ----------------------------
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# ----------------------------
# 2. SERVO PINS AND POSITIONS
# ----------------------------
servo_pins = {
    "Hip Left": 23,
    "Knee Left": 22,
    "Hip Right": 27,
    "Knee Right": 17,  # Physically reversed
    "Left Toe": 16,
    "Right Toe": 26,   # Physically reversed
}

natural_standing_position = {
    "Hip Left": 90,
    "Knee Left": 120,
    "Hip Right": 90,
    "Knee Right": 60,
    "Left Toe": 110,
    "Right Toe": 110
}

# (Optional) Full walking cycle for automated Start/Stop
walking_cycle = [
    # Step 1: Lift left leg
    {"Hip Left": 60, "Knee Left": 140,
     "Hip Right": 90, "Knee Right": 60,
     "Left Toe": 95, "Right Toe": 110},

    # Step 2: Left toe down
    {"Hip Left": 60, "Knee Left": 140,
     "Hip Right": 90, "Knee Right": 60,
     "Left Toe": 80, "Right Toe": 110},

    # Step 3: Bring left leg back, start lifting right leg
    {"Hip Left": 90, "Knee Left": 120,
     "Hip Right": 60, "Knee Right": 140,
     "Left Toe": 110, "Right Toe": 95},

    # Step 4: Right toe down (for example)
    {"Hip Left": 90, "Knee Left": 120,
     "Hip Right": 60, "Knee Right": 140,
     "Left Toe": 110, "Right Toe": 80},

    # Step 5: Bring right leg back
    {"Hip Left": 90, "Knee Left": 120,
     "Hip Right": 90, "Knee Right": 60,
     "Left Toe": 110, "Right Toe": 110},
]

walking = False  # Controls the walking cycle loop

# ----------------------------
# 3. SERVO HELPER FUNCTIONS
# ----------------------------
def set_servo_angle(pin, angle, reverse=False):
    """Move the servo on 'pin' to 'angle'. If reverse=True, invert the angle."""
    if reverse:
        angle = 180 - angle
    pulsewidth = 500 + (angle / 180.0) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))  # clamp to [500..2500]
    pi.set_servo_pulsewidth(pin, pulsewidth)

def move_all_servos(angles):
    """Move each servo to the specified angle; reverse Right Knee and Right Toe."""
    for joint, angle in angles.items():
        reverse = (joint == "Right Knee" or joint == "Right Toe")
        set_servo_angle(servo_pins[joint], angle, reverse)
        print(f"{joint} moved to {angle}°")

def update_text_boxes(angles):
    """Update all text boxes (GUI entries) with the values in 'angles'."""
    for joint, angle in angles.items():
        servo_angles[joint].set(angle)

# ----------------------------
# 4. STEP FUNCTIONS
# ----------------------------
def step_right_leg_up():
    """
    Move only the right leg servos to a 'leg up' position.
    Then update the text boxes with the new angles.
    """
    # Read current angles from GUI
    current_angles = {joint: servo_angles[joint].get() for joint in servo_angles}

    # Modify only the right leg angles
    current_angles["Hip Right"]  = 50
    current_angles["Knee Right"] = 50
    current_angles["Right Toe"]  = 95

    move_all_servos(current_angles)
    # Update text boxes to show new angles
    update_text_boxes(current_angles)

    messagebox.showinfo("Step", "Right leg moved up.")

def step_right_knee_bend_more():
    """
    Further bend the right knee and slightly adjust the toe.
    Then update the text boxes with the new angles.
    """
    current_angles = {joint: servo_angles[joint].get() for joint in servo_angles}

    current_angles["Knee Right"] = 150
    current_angles["Right Toe"]  = 90

    move_all_servos(current_angles)
    update_text_boxes(current_angles)

    messagebox.showinfo("Step", "Right knee bent more, toe adjusted.")

def step_right_toe_down():
    """
    Lower the right toe a bit while returning knee closer to normal.
    Then update the text boxes with the new angles.
    """
    current_angles = {joint: servo_angles[joint].get() for joint in servo_angles}

    current_angles["Knee Right"] = 130
    current_angles["Right Toe"]  = 85

    move_all_servos(current_angles)
    update_text_boxes(current_angles)

    messagebox.showinfo("Step", "Right toe lowered, knee partially undone.")

# ----------------------------
# 5. RESET & FULL-CYCLE METHODS
# ----------------------------
def reset_to_natural_position():
    """Reset all servos to the natural standing position and update text fields."""
    update_text_boxes(natural_standing_position)
    move_all_servos(natural_standing_position)
    messagebox.showinfo("Reset", "Robot has been reset to the natural standing position.")

def execute_walking_cycle():
    """Execute the walking cycle in a loop until 'walking' is set to False."""
    global walking
    walking = True
    while walking:
        for step in walking_cycle:
            if not walking:
                break
            move_all_servos(step)
            # Also update text boxes for clarity
            update_text_boxes(step)
            time.sleep(0.5)
    messagebox.showinfo("Cycle Stopped", "The walking cycle has been stopped.")

def start_cycle():
    """Start the walking cycle in a separate thread."""
    global walking
    if not walking:
        walking_thread = threading.Thread(target=execute_walking_cycle)
        walking_thread.start()

def stop_cycle():
    """Stop the walking cycle."""
    global walking
    walking = False

# ----------------------------
# 6. TKINTER GUI SETUP
# ----------------------------
root = tk.Tk()
root.title("Robot Servo Control")
root.geometry("600x480")

style = ttk.Style(root)
style.theme_use("clam")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

title_label = ttk.Label(main_frame, text="Robot Servo Control", font=("Helvetica", 16))
title_label.grid(column=0, row=0, columnspan=3, pady=10)

# ----------------------------
# 6A. STEP BUTTONS
# ----------------------------
step_button_1 = ttk.Button(main_frame, text="Step 1: Right Leg Up", command=step_right_leg_up)
step_button_1.grid(column=0, row=1, padx=5, pady=5)

step_button_2 = ttk.Button(main_frame, text="Step 2: Bend Right Knee More", command=step_right_knee_bend_more)
step_button_2.grid(column=1, row=1, padx=5, pady=5)

step_button_3 = ttk.Button(main_frame, text="Step 3: Toe Down", command=step_right_toe_down)
step_button_3.grid(column=2, row=1, padx=5, pady=5)

# ----------------------------
# 6B. FULL CYCLE BUTTONS
# ----------------------------
start_cycle_button = ttk.Button(main_frame, text="Start Walking Cycle", command=start_cycle)
start_cycle_button.grid(column=0, row=2, padx=5, pady=10, sticky=tk.E)

stop_cycle_button = ttk.Button(main_frame, text="Stop Walking Cycle", command=stop_cycle)
stop_cycle_button.grid(column=1, row=2, padx=5, pady=10, sticky=tk.W)

reset_button = ttk.Button(main_frame, text="Reset to Natural Position", command=reset_to_natural_position)
reset_button.grid(column=2, row=2, padx=5, pady=10)

# ----------------------------
# 7. ANGLE ADJUSTMENT SECTION
# ----------------------------
angle_frame = ttk.LabelFrame(main_frame, text="Servo Angles", padding="10")
angle_frame.grid(column=0, row=3, columnspan=3, pady=10, sticky=(tk.W, tk.E))

servo_angles = {
    "Hip Left":   tk.DoubleVar(value=natural_standing_position["Hip Left"]),
    "Knee Left":  tk.DoubleVar(value=natural_standing_position["Knee Left"]),
    "Hip Right":  tk.DoubleVar(value=natural_standing_position["Hip Right"]),
    "Knee Right": tk.DoubleVar(value=natural_standing_position["Knee Right"]),
    "Left Toe":   tk.DoubleVar(value=natural_standing_position["Left Toe"]),
    "Right Toe":  tk.DoubleVar(value=natural_standing_position["Right Toe"]),
}

def update_servo_angles():
    """Move the servos to the angles specified in the text fields."""
    angles = {joint: var.get() for joint, var in servo_angles.items()}
    move_all_servos(angles)
    messagebox.showinfo("Updated", "Servo angles updated!")
    # After moving, ensure text boxes remain consistent (already done, but in case you modify angles)
    update_text_boxes(angles)

row_index = 0
for joint, var in servo_angles.items():
    ttk.Label(angle_frame, text=joint).grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
    ttk.Entry(angle_frame, textvariable=var, width=5).grid(row=row_index, column=1, padx=5, pady=5)
    row_index += 1

update_button = ttk.Button(angle_frame, text="Update Angles", command=update_servo_angles)
update_button.grid(column=0, row=row_index, columnspan=2, pady=10)

# ----------------------------
# 8. MAINLOOP AND CLEANUP
# ----------------------------
root.mainloop()

# On close: turn off all servos
for pin in servo_pins.values():
    pi.set_servo_pulsewidth(pin, 0)
pi.stop()
print("pigpio cleanup complete.")
