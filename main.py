import datetime
import json
import os
import pandas as pd
import serial
import time
import toml
import winsound

data = list()


def main():
    global data
    # dir setting
    now = datetime.datetime.now().strftime('%Y_%m%d_%H%M')
    make_dir("data")
    csv_path = "data/" + now + ".csv"

    # sensordata setting
    obj = toml.load("settings.toml")
    PORT_NUM = obj["sensor_settings"]["PORT_NUM"]
    SERIAL_BPS = obj["sensor_settings"]["SERIAL_BPS"]
    EXECUTION_TIME = obj["video_settings"]["TIME"]
    ser = serial.Serial(PORT_NUM, SERIAL_BPS, timeout=0.1)
    line = ser.readline()

    print('Serial warming up...')
    time.sleep(2)

    make_sound(2000, 100, 1)
    start_time = time.time()
    while time.time()-start_time < EXECUTION_TIME:
        line = ser.readline()
        add_data_at_intervals(line)
        time.sleep(0.1)
        save_to_csv(csv_path, data)
    make_sound(2000, 100, 2)


def make_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)


def add_data_at_intervals(line):
    global data
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')

    if line == "":
        return
    line_disp = line.strip().decode('UTF-8').split(',')

    if len(line_disp) == 7:
        tmp_line = list()
        for i in range(7):
            # 空白''が入っていないときだけ記録
            if line_disp[i] != '':
                tmp_line.append(float(line_disp[i]))
            else:
                return
        tmp_line.insert(0, now)

        print(tmp_line)
        data.append(tmp_line)


def save_to_csv(csv_path, data):
    SENSORDATA_LABEL = list()
    json_path = "config/sensordata_label.json"

    with open(json_path, "r", encoding="utf-8") as f:
        df = json.load(f)
        for i in range(len(df["sensordata_label"])):
            SENSORDATA_LABEL.append(df["sensordata_label"][i])
    df = pd.DataFrame(data=data, columns=SENSORDATA_LABEL)
    df.to_csv(csv_path)


def make_sound(frequency, duration, counts):
    for count in range(counts):
        winsound.Beep(frequency, duration)


if __name__ == "__main__":
    main()
