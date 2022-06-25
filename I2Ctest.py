import serial

ser = serial.Serial('COM3', 115200, timeout=0.1)
data = ser.read_all()
print(data)
ser.close()
