import serial
import time
import pandas as pd
import datetime
import os
import winsound

data = list()


def main():
    # settings
    global data
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    csv_path = setup_csv_path()

    print('Serial warming up...')
    line = ser.readline()
    time.sleep(2)

    start_time = time.time()
    while time.time()-start_time < 90:
        line = ser.readline()
        line_disp = line.strip().decode('UTF-8')
        add_data_at_intervals(line_disp)

        # 0.1秒くらいで、ずっとデータを取り続けられる。
        time.sleep(0.1)
        save_to_csv(csv_path, data)
    frequency = 2000
    duration = 1000
    winsound.Beep(frequency, duration)


def add_data_at_intervals(line_disp):
    global data
    line_disp = line_disp.split(',')

    time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')

    if len(line_disp) == 7:
        tmp_float_line = list()
        for i in range(7):
            # 空白''が入っていないときだけ記録
            if line_disp[i] != '':
                tmp_float_line.append(float(line_disp[i]))
            else:
                return
        tmp_float_line.insert(0, time)

        print(tmp_float_line)
        data.append(tmp_float_line)


def save_to_csv(csv_path, data):
    df = pd.DataFrame(data=data, columns=[
                      "time", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z", "light"])

    if os.path.exists("data/csv") == False:
        os.mkdir("data/csv")
    if os.path.isdir(csv_path) == True:
        os.remove(csv_path)
    df.to_csv(csv_path)


def setup_csv_path():
    time = datetime.datetime.now().strftime('%Y_%m%d_%H%M')
    if os.path.exists("data/csv") == False:
        os.mkdir("data/csv")
    csv_path = f"data/csv/{time}.csv"
    if os.path.exists(csv_path) == True:
        print("1分後待ってプログラムを動かしてください\n")
        exit()
    return csv_path


if __name__ == "__main__":
    main()
