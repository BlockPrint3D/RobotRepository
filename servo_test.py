from time import sleep
from adafruit_servokit import ServoKit

def alternating_servo_test(pin1, pin2, servo_name1, servo_name2):
    print(f"Testing {servo_name1} and {servo_name2} alternating...")
    for angle in range(0, 181, 10):
        set_servo_angle(pin1, angle)
        set_servo_angle(pin2, 180 - angle)
        print(f"{servo_name1} at {angle} degrees, {servo_name2} at {180 - angle} degrees")
        time.sleep(0.1)
    print(f"{servo_name1} and {servo_name2} max angles reached.")

def step_up_test(pin, servo_name):
    print(f"Testing {servo_name} step-up motion...")
    for angle in range(0, 181, 15):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    print(f"{servo_name} max angle reached: 180 degrees")

def step_down_test(pin, servo_name):
    print(f"Testing {servo_name} step-down motion...")
    for angle in range(180, -1, -15):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    print(f"{servo_name} min angle reached: 0 degrees")

def quick_reverse_test(pin, servo_name):
    print(f"Testing {servo_name} with quick reverse...")
    for angle in range(0, 181, 20):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    for angle in range(180, -1, -20):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    print(f"{servo_name} max angle reached: 180 degrees")

def wiggle_test(pin, servo_name):
    print(f"Testing {servo_name} with wiggle motion...")
    for _ in range(10):  # 10 random wiggles
        angle = random.randint(0, 180)
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.05)
    print(f"{servo_name} max angle reached: 180 degrees")

def gradual_reverse_test(pin, servo_name):
    print(f"Testing {servo_name} gradual reverse motion...")
    for angle in range(180, -1, 5):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)
    print(f"{servo_name} min angle reached: 0 degrees")

def slow_oscillation_test(pin, servo_name):
    print(f"Testing {servo_name} slow oscillation...")
    for i in range(0, 360, 10):
        angle = int(90 + 90 * math.sin(math.radians(i)))
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)
    print(f"{servo_name} max angle reached: 180 degrees")

def complex_pattern_test(pin, servo_name):
    print(f"Testing {servo_name} with complex pattern...")
    for i in range(10):  # 10 cycles of different patterns
        angle = random.randint(0, 180)
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
        angle = random.randint(0, 180)
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.15)
    print(f"{servo_name} max angle reached: 180 degrees")

def alternating_high_low_test(pin, servo_name):
    print(f"Testing {servo_name} with alternating high and low positions...")
    for _ in range(5):  # 5 times alternating
        set_servo_angle(pin, 0)
        print(f"{servo_name} at 0 degrees")
        time.sleep(0.5)
        set_servo_angle(pin, 180)
        print(f"{servo_name} at 180 degrees")
        time.sleep(0.5)
    print(f"{servo_name} max angle reached: 180 degrees")

def rotate_test(pin, servo_name):
    print(f"Testing {servo_name} with full rotation motion...")
    for angle in range(0, 181, 30):  # Full rotation steps
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.15)
    for angle in range(180, -1, -30):  # Return to 0 degrees
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.15)
    print(f"{servo_name} max angle reached: 180 degrees")

def zigzag_motion_test(pin, servo_name):
    print(f"Testing {servo_name} with zigzag motion...")
    for i in range(10):  # 10 zigzags
        angle = 180 if i % 2 == 0 else 0
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)
    print(f"{servo_name} max angle reached: 180 degrees")

def increasing_speed_test(pin, servo_name):
    print(f"Testing {servo_name} with increasing speed...")
    for angle in range(0, 181, 10):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2 - (angle / 180.0) * 0.15)
    for angle in range(180, -1, -10):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2 - (angle / 180.0) * 0.15)
    print(f"{servo_name} max angle reached: 180 degrees")

def large_step_motion_test(pin, servo_name):
    print(f"Testing {servo_name} with large step motion...")
    for angle in range(0, 181, 30):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    for angle in range(180, -1, -30):
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.1)
    print(f"{servo_name} max angle reached: 180 degrees")

def bounce_motion_test(pin, servo_name):
    print(f"Testing {servo_name} with bounce motion...")
    for i in range(10):  # Bounce 10 times
        angle = 0 if i % 2 == 0 else 180
        set_servo_angle(pin, angle)
        print(f"{servo_name} at {angle} degrees")
        time.sleep(0.2)
    print(f"{servo_name} max angle reached: 180 degrees")

# Combine all test functions and continue expanding
try:
    # Slow test: Test each servo by moving it from 0 to max angle and back
    for servo, pin in servo_pins.items():
        slow_test_servo(pin, servo)

    # Fast test: Test each servo by moving it from 0 to max angle and back quickly
    for servo, pin in servo_pins.items():
        fast_test_servo(pin, servo)

    # Additional tests
    for servo, pin in servo_pins.items():
        random_test_servo(pin, servo)
        sine_wave_test_servo(pin, servo)
        back_and_forth_test_servo(pin, servo)
        dynamic_speed_test_servo(pin, servo)
        pause_between_movements(pin, servo)
        repeat_pattern_test_servo(pin, servo)
        oscillating_motion_test(pin, servo)
        cross_servo_motion(pin, pin, "Hip Left", "Knee Right")
        alternating_servo_test(pin, pin, "Hip Left", "Knee Left")
        step_up_test(pin, "Hip Left")
        step_down_test(pin, "Knee Right")
        quick_reverse_test(pin, "Knee Left")
        wiggle_test(pin, "Hip Right")
        gradual_reverse_test(pin, "Knee Left")
        slow_oscillation_test(pin, "Hip Left")
        complex_pattern_test(pin, "Hip Right")
        alternating_high_low_test(pin, "Knee Right")
        rotate_test(pin, "Hip Right")
        zigzag_motion_test(pin, "Knee Left")
        increasing_speed_test(pin, "Knee Right")
        large_step_motion_test(pin, "Hip Left")
        bounce_motion_test(pin, "Hip Right")

    # After testing, set all servos back to 90 degrees
    set_all_to_90()

finally:
    # Cleanup
    for pin in servo_pins.values():
        pi.set_servo_pulsewidth(pin, 0)  # Stop PWM signal to the servos
    
    pi.stop()  # Disconnect from pigpio
    print("pigpio cleanup complete.")
