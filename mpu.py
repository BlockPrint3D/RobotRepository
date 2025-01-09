import smbus
import time
import math
import tkinter as tk

# MPU6050 Registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus.SMBus(1)  # I2C bus 1 on newer Pis

def init_mpu():
    # Wake up MPU6050
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    # Read two bytes of data from 'addr'
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value

init_mpu()

# Create the main window
root = tk.Tk()
root.title("MPU6050 Sensor Data")

# Labels to display Pitch, Roll, and Gyro Data
pitch_label = tk.Label(root, text="Pitch: -- °", font=("Helvetica", 14))
roll_label = tk.Label(root, text="Roll: -- °", font=("Helvetica", 14))
gx_label = tk.Label(root, text="gx: -- °/s", font=("Helvetica", 14))
gy_label = tk.Label(root, text="gy: -- °/s", font=("Helvetica", 14))
gz_label = tk.Label(root, text="gz: -- °/s", font=("Helvetica", 14))

pitch_label.pack(pady=5)
roll_label.pack(pady=5)
gx_label.pack(pady=5)
gy_label.pack(pady=5)
gz_label.pack(pady=5)

def update_data():
    # Read accelerometer raw values
    ax = read_raw_data(ACCEL_XOUT_H)
    ay = read_raw_data(ACCEL_XOUT_H + 2)
    az = read_raw_data(ACCEL_XOUT_H + 4)

    # Read gyroscope raw values
    gx = read_raw_data(GYRO_XOUT_H)
    gy = read_raw_data(GYRO_XOUT_H + 2)
    gz = read_raw_data(GYRO_XOUT_H + 4)

    # Convert to 'g' for accelerometer and '°/s' for gyroscope
    ax_g = ax/16384.0
    ay_g = ay/16384.0
    az_g = az/16384.0

    gx_dps = gx/131.0
    gy_dps = gy/131.0
    gz_dps = gz/131.0

    # Compute pitch and roll from accelerometer data as a starting point
    pitch = math.degrees(math.atan2(ax_g, math.sqrt(ay_g*ay_g + az_g*az_g)))
    roll = math.degrees(math.atan2(ay_g, az_g))

    # Update labels
    pitch_label.config(text=f"Pitch: {pitch:.2f}°")
    roll_label.config(text=f"Roll: {roll:.2f}°")
    gx_label.config(text=f"gx: {gx_dps:.2f}°/s")
    gy_label.config(text=f"gy: {gy_dps:.2f}°/s")
    gz_label.config(text=f"gz: {gz_dps:.2f}°/s")

    # Schedule the next update in 500 ms
    root.after(500, update_data)

# Start updating data
update_data()

# Run the GUI mainloop
root.mainloop()
