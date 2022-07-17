import cv2
import datetime
import json
import os
import pandas as pd
import serial
import time
import toml

data = list()


def main():
    global data

    # dir setting
    now = datetime.datetime.now().strftime('%Y_%m%d_%H%M')
    make_dir(now)
    csv_path = "data/" + now + "/sensor_data.csv"
    video_path = "data/" + now + "/video.mp4"

    # video setting
    obj = toml.load("settings.toml")
    EXECUTION_TIME = obj["video_settings"]["TIME"]
    VIDEO_FPS = obj["video_settings"]["FPS"]
    CAMERA_NUM = obj["video_settings"]["CAMERA_NUM"]
    cap = cv2.VideoCapture(CAMERA_NUM)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(video_path, fourcc, VIDEO_FPS, (width, height))

    # sensordata setting
    PORT_NUM = obj["sensor_settings"]["PORT_NUM"]
    SERIAL_BPS = obj["sensor_settings"]["SERIAL_BPS"]
    ser = serial.Serial(PORT_NUM, SERIAL_BPS, timeout=0.1)
    line = ser.readline()

    # exclude no value data
    print('Serial warming up...')
    time.sleep(2)

    # loop
    tmp_time = time.time()
    roop = int(VIDEO_FPS * EXECUTION_TIME)
    for i in range(roop):
        # video
        ret, frame = cap.read()
        video.write(frame)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        # sensordata
        line = ser.readline()
        add_data_at_intervals(line)
        save_to_csv(csv_path, data)
        print(time.time()-tmp_time)
        tmp_time = time.time()

    print("STOP")
    video.release()
    cap.release()
    cv2.destroyAllWindows()


def make_dir(now):
    path = "data/" + now
    if os.path.exists(path) is True:
        print("1分後待ってプログラムを動かしてください\n")
        exit()
    os.mkdir(path)


def add_data_at_intervals(line):
    global data
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')

    if line == "":
        return
    line_disp = line.strip().decode('UTF-8')
    line_disp = line_disp.split(',')
    # print(line_disp)
    if len(line_disp) == 7:
        tmp_line = list()
        for i in range(7):
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


if __name__ == "__main__":
    main()
