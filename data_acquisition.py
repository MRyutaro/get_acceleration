import datetime
import json
import pandas as pd
import serial
import time

data = list()


def main():
    global data
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    csv_path = setup_csv_path()

    print('Serial warming up...')
    line = ser.readline()
    time.sleep(2)

    while True:
        line = ser.readline()
        line_disp = line.strip().decode('UTF-8')
        add_data_at_intervals(line_disp)

        # 0.1秒くらいで、ずっとデータを取り続けられる。
        time.sleep(0.1)
        save_to_csv(csv_path, data)


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
    SENSORDATA_LABEL = list()
    path = "config/sensordata_label.json"
    with open(path, "r", encoding="utf-8") as f:
        df = json.load(f)
        for i in range(len(df["sensordata_label"])):
            SENSORDATA_LABEL.append(df["sensordata_label"][i])
    df = pd.DataFrame(data=data, columns=SENSORDATA_LABEL)

    # if os.path.exists("data/csv") is False:
    #     os.mkdir("data/csv")
    # if os.path.isdir(csv_path) is True:
    #     os.remove(csv_path)
    df.to_csv(csv_path)


def setup_csv_path():
    now = datetime.datetime.now().strftime('%Y_%m%d_%H%M')
    csv_path = f"data/{now}/sensor_data.csv"
    return csv_path


if __name__ == "__main__":
    main()
