import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize I2C bus and PCA9685 module
i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c)

# Set the PWM frequency to 50Hz (typical for servos)
pwm.frequency = 50

# Function to set the angle of a servo
def set_servo_angle(channel, angle):
    pulse_min = 500   # Min pulse length in microseconds
    pulse_max = 2500  # Max pulse length in microseconds

    pulse_length = int(pulse_min + (angle / 180.0) * (pulse_max - pulse_min))
    pwm_value = int(pulse_length * 4096 / 20000)  # 20ms period at 50Hz

    pwm.channels[channel].duty_cycle = pwm_value
    servo_positions[channel] = angle  # Store the current angle

# Initialize servo positions
servo_positions = [0] * 6

# Function to control servos from SSH (console input)
def control_servos():
    while True:
        print("\nServo Controller:")
        for i in range(6):
            print(f"Servo {i}: {servo_positions[i]}°")
        
        try:
            servo_id = int(input("Enter the servo number (0-5) to control or -1 to exit: "))
            if servo_id == -1:
                break
            if servo_id < 0 or servo_id > 5:
                print("Invalid servo number. Please choose between 0 and 5.")
                continue
            
            angle = int(input(f"Enter the angle for Servo {servo_id} (0-180): "))
            if 0 <= angle <= 180:
                set_servo_angle(servo_id, angle)
                print(f"Servo {servo_id} set to {angle}°")
            else:
                print("Invalid angle. Please enter a value between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

# Run the servo control function
control_servos()

# Turn off all servos on exit
for channel in range(6):
    pwm.channels[channel].duty_cycle = 0
