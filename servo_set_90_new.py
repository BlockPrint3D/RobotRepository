import time
from adafruit_servokit import ServoKit

# Constants
nbPCAServo = 16

# Objects
pca = ServoKit(channels=16)

# Function init
def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(500, 2500)

# Function pcaScenario
def pcaScenario():
    """Move all servos to 90°, then 0°, then 90°"""
    for i in range(nbPCAServo):
        print(f"Servo {i} to 90°")
        pca.servo[i].angle = 90
        time.sleep(0.5)
        print(f"Servo {i} to 0°")
        pca.servo[i].angle = 0
        time.sleep(0.5)
        print(f"Servo {i} back to 90°")
        pca.servo[i].angle = 90
        time.sleep(0.5)

# Main function
def main():
    init()
    pcaScenario()

if __name__ == '__main__':
    main()
