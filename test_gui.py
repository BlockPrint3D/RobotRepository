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

def generate_large_stride_cycle():
    """Generate a walking cycle with consistent and extended leg movements."""
    return [
        # Step 1: Lift and move left leg forward, keep right leg stable
        {"Hip Left": 50, "Knee Left": 160, "Hip Right": 50, "Knee Right": 50, "Left Toe": 70, "Right Toe": 95},

        # Step 2: Plant left leg, start lifting right leg
        {"Hip Left": 50, "Knee Left": 140, "Hip Right": 50, "Knee Right": 50, "Left Toe": 80, "Right Toe": 95},

        # Step 3: Move right leg forward, left leg stable
        {"Hip Left": 90, "Knee Left": 120, "Hip Right": 50, "Knee Right": 50, "Left Toe": 110, "Right Toe": 95},

        # Step 4: Plant right leg, reset left leg
        {"Hip Left": 70, "Knee Left": 140, "Hip Right": 50, "Knee Right": 50, "Left Toe": 90, "Right Toe": 95},

        # Step 5: Reset to natural standing position
        {"Hip Left": 90, "Knee Left": 120, "Hip Right": 50, "Knee Right": 50, "Left Toe": 110, "Right Toe": 95},
    ]


#walking_cycle = [
#    {"Hip Left": 60, "Knee Left": 140, "Hip Right": 90, "Knee Right": 120, "Left Toe": 95, "Right Toe": 95},
#    {"Hip Left": 60, "Knee Left": 140, "Hip Right": 90, "Knee Right": 120, "Left Toe": 80, "Right Toe": 100},
#    {"Hip Left": 90, "Knee Left": 120, "Hip Right": 60, "Knee Right": 140, "Left Toe": 110, "Right Toe": 85},
#    {"Hip Left": 90, "Knee Left": 120, "Hip Right": 60, "Knee Right": 140, "Left Toe": 110, "Right Toe": 80},
#    {"Hip Left": 90, "Knee Left": 120, "Hip Right": 90, "Knee Right": 120, "Left Toe": 110, "Right Toe": 95},
#]

walking_cycle = generate_large_stride_cycle()


walking = False
walking_thread = None

# ----------------------------
# 3. SERVO HELPER FUNCTIONS
# ----------------------------
def set_servo_angle(pin, angle, reverse=False):
    """Move the servo on 'pin' to 'angle'. If reverse=True, invert the angle."""
    try:
        if reverse:
            angle = 180 - angle
        pulsewidth = 500 + (angle / 180.0) * 2000
        pulsewidth = max(500, min(2500, pulsewidth))  # clamp to [500..2500]
        pi.set_servo_pulsewidth(pin, pulsewidth)
    except Exception as e:
        print(f"Error setting servo angle: {e}")

def move_all_servos(angles):
    """Move each servo to the specified angle; reverse Right Knee and Right Toe."""
    for joint, angle in angles.items():
        reverse = (joint == "Right Knee" or joint == "Right Toe")
        set_servo_angle(servo_pins[joint], angle, reverse)
        time.sleep(0.05)  # Small delay between servo movements

def interpolate_positions(start, end, steps):
    """
    Interpolates between start and end positions over the specified number of steps.
    Returns a list of intermediate positions.
    """
    interpolated_positions = []
    for step in range(steps):
        intermediate = {
            joint: start[joint] + (end[joint] - start[joint]) * step / steps
            for joint in start
        }
        interpolated_positions.append(intermediate)
    return interpolated_positions

# ----------------------------
# 4. RESET & WALKING FUNCTIONS
# ----------------------------
def reset_to_natural_position():
    """Reset all servos to the natural standing position."""
    move_all_servos(natural_standing_position)
    messagebox.showinfo("Reset", "Robot reset to natural position.")

def execute_walking_cycle():
    """Execute the walking cycle with extended leg movements."""
    global walking
    try:
        while walking:
            for i in range(len(walking_cycle) - 1):
                start = walking_cycle[i]
                end = walking_cycle[i + 1]
                interpolated_positions = interpolate_positions(start, end, steps=5)
                for position in interpolated_positions:
                    if not walking:
                        break
                    move_all_servos(position)
                    time.sleep(0.15)  # Slightly faster transition
    except Exception as e:
        print(f"Error during walking cycle: {e}")
    finally:
        reset_to_natural_position()




def start_cycle():
    """Start the walking cycle in a separate thread."""
    global walking, walking_thread
    if not walking:
        walking = True
        walking_thread = threading.Thread(target=execute_walking_cycle, daemon=True)
        walking_thread.start()

def stop_cycle():
    """Stop the walking cycle."""
    global walking
    walking = False

# ----------------------------
# 5. TKINTER GUI SETUP
# ----------------------------
root = tk.Tk()
root.title("Robot Servo Control")
root.geometry("600x480")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Step Buttons
ttk.Button(main_frame, text="Start Walking Cycle", command=start_cycle).grid(column=0, row=1, padx=5, pady=5)
ttk.Button(main_frame, text="Stop Walking Cycle", command=stop_cycle).grid(column=1, row=1, padx=5, pady=5)
ttk.Button(main_frame, text="Reset to Natural Position", command=reset_to_natural_position).grid(column=2, row=1, padx=5, pady=5)

# ----------------------------
# 6. CLEANUP ON EXIT
# ----------------------------
def on_close():
    """Ensure servos are turned off and pigpio is cleaned up on exit."""
    stop_cycle()
    if walking_thread:
        walking_thread.join()
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
