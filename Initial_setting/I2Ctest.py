import serial
import time

ser = serial.Serial('COM3', 115200, timeout=0.1)
line = ser.readline()

while True:
    line = ser.readline()
    line_disp = line.strip().decode('UTF-8')
    line_disp = line_disp.split(',')
    if len(line_disp) == 7:
        accel = "【加速度】x:" + line_disp[0] + " y:" + \
            line_disp[1] + " z:" + line_disp[2]
        gyro = "【角速度】x:" + line_disp[3] + " y:" + \
            line_disp[4] + " z:" + line_disp[5]
        light = "【ライト】" + line_disp[6]
        print(accel + gyro + light)
    time.sleep(0.2)
