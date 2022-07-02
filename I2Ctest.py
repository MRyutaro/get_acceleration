import serial
import time

ser = serial.Serial('COM3', 115200, timeout=0.1)
line = ser.readline()

while True:
    line = ser.readline()
    line_disp = line.strip().decode('UTF-8')
    print(line_disp)
    time.sleep(0.2)
