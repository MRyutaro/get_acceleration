import datetime
import glob
import json
import os
import pandas as pd
import serial
import shutil
import time
import toml
import winsound

import draw_graph


def main():
    # フォルダの設定
    now = datetime.datetime.now().strftime('%Y_%m%d_%H%M')
    make_dir("data")
    csv_path = "data/" + now + ".csv"

    # センサーデータの設定
    obj = toml.load("settings.toml")
    PORT_NUM = obj["sensor_settings"]["PORT_NUM"]
    SERIAL_BPS = obj["sensor_settings"]["SERIAL_BPS"]
    EXECUTION_TIME = obj["video_settings"]["TIME"]
    ser = serial.Serial(PORT_NUM, SERIAL_BPS, timeout=0.1)
    sensor_data = ser.readline()
    all_data = list()

    sec, data_list, lines, ax = draw_graph.setup_graph(
        sensor_data)

    print('Serial warming up...')
    time.sleep(2)

    make_sound(2000, 100, 1)
    start_time = time.time()
    while time.time()-start_time < EXECUTION_TIME:
        sensor_data = ser.readline()
        sec, data_list, lines, ax = draw_graph.draw_graph(
            sensor_data, sec, data_list, lines, ax)
        all_data = add_data_at_intervals(sensor_data, all_data)
        save_to_csv(csv_path, all_data)
    move_and_rename_video()
    make_sound(2000, 100, 2)


def make_sound(frequency, duration, counts):
    for count in range(counts):
        winsound.Beep(frequency, duration)


def make_dir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)


def add_data_at_intervals(sensor_data, all_data):
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
    if sensor_data == " ":
        return all_data

    sensor_data = sensor_data.strip().decode("UTF-8").split(",")
    if len(sensor_data) == 7:
        tmp_line = list()
        for i in range(7):
            if sensor_data[i] == " ":
                return
            else:
                tmp_line.append(float(sensor_data[i]))
        tmp_line.insert(0, now)

        print(tmp_line)
        all_data.append(tmp_line)
    return all_data


def save_to_csv(csv_path, data):
    SENSORDATA_LABEL = list()
    json_path = "config/sensordata_label.json"

    with open(json_path, "r", encoding="UTF-8") as f:
        df = json.load(f)
        for i in range(len(df["sensordata_label"])):
            SENSORDATA_LABEL.append(df["sensordata_label"][i])
    df = pd.DataFrame(data=data, columns=SENSORDATA_LABEL)
    df.to_csv(csv_path)


def move_and_rename_video():
    obj = toml.load("settings.toml")
    VIDEO_DIR = obj["video_settings"]["VIDEO_DIR"]

    for file in glob.glob(VIDEO_DIR + "/*.mp4"):
        shutil.move(file, "./data")
        no_file = file[39:53].replace("_", "")
        new_file_name = no_file[:4] + "_" + no_file[4:8] + "_" + no_file[8:12]
        old_file_name = file[35:]
        old_file_path = "data/" + old_file_name
        new_file_path = "data/" + new_file_name + ".mp4"
        os.rename(old_file_path, new_file_path)


if __name__ == "__main__":
    main()
