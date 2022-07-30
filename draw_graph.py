import matplotlib.pyplot as plt
import numpy as np
import serial


def main():
    # データの取得
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    sensor_data = ser.readline()
    sec, data_list, lines, ax = setup_graph(
        sensor_data)
    while True:
        sensor_data = ser.readline()
        sec, data_list, lines, ax = draw_graph(
            sensor_data, sec, data_list, lines, ax)


def setup_graph(sensor_data):
    sensor_data = sensor_data.strip().decode('UTF-8').split(',')

    # センサーデータ取得
    accel_data = [0]*3
    gyro_data = [0]*3

    fig, (ax_accel, ax_gyro) = plt.subplots(ncols=2, figsize=(6, 4))

    # x座標
    sec = np.arange(-np.pi, np.pi, 0.1)

    # y座標
    accel_list_x = np.zeros(63)
    accel_list_x[0] = accel_data[0]
    accel_x_lines, = ax_accel.plot(sec, accel_list_x, color="red", label="x")

    accel_list_y = np.zeros(63)
    accel_list_y[0] = accel_data[1]
    accel_y_lines, = ax_accel.plot(sec, accel_list_y, color="blue", label="y")

    accel_list_z = np.zeros(63)
    accel_list_z[0] = accel_data[2]
    accel_z_lines, = ax_accel.plot(sec, accel_list_z, color="green", label="z")

    gyro_list_x = np.zeros(63)
    gyro_list_x[0] = gyro_data[0]
    gyro_x_lines, = ax_gyro.plot(sec, gyro_list_x, color="red", label="x")

    gyro_list_y = np.zeros(63)
    gyro_list_y[0] = gyro_data[1]
    gyro_y_lines, = ax_gyro.plot(sec, gyro_list_y, color="blue", label="y")

    gyro_list_z = np.zeros(63)
    gyro_list_z[0] = gyro_data[2]
    gyro_z_lines, = ax_gyro.plot(sec, gyro_list_z, color="green", label="z")

    # 軸設定
    ax_accel.legend()  # ラベル描画
    ax_accel.set_title("accel")
    ax_accel.set_ylim(-4, 4)
    ax_accel.set_xticks([])  # X軸のメモリ非表示

    ax_gyro.legend()  # ラベル描画
    ax_gyro.set_title("gyro")
    ax_gyro.set_ylim(-300, 300)
    ax_gyro.set_xticks([])  # X軸のメモリ非表示

    data_list = [[accel_list_x, accel_list_y, accel_list_z],
                 [gyro_list_x, gyro_list_y, gyro_list_z]]
    lines = [[accel_x_lines, accel_y_lines, accel_z_lines],
             [gyro_x_lines, gyro_y_lines, gyro_z_lines]]
    ax = [ax_accel, ax_gyro]

    return sec, data_list, lines, ax


def draw_graph(sensor_data, sec, data_list, lines, ax):
    sensor_data = sensor_data.strip().decode('UTF-8').split(',')

    if len(sensor_data) != 7:
        return sec, data_list, lines, ax
    else:
        # センサーデータ取得
        accel_data = [sensor_data[0], sensor_data[1], sensor_data[2]]
        gyro_data = [sensor_data[3], sensor_data[4], sensor_data[5]]

        # データの更新
        sec += 0.1

        data_list[0][0] = np.roll(data_list[0][0], 1)
        data_list[0][0][0] = accel_data[0]
        data_list[0][1] = np.roll(data_list[0][1], 1)
        data_list[0][1][0] = accel_data[1]
        data_list[0][2] = np.roll(data_list[0][2], 1)
        data_list[0][2][0] = accel_data[2]

        data_list[1][0] = np.roll(data_list[1][0], 1)
        data_list[1][0][0] = gyro_data[0]
        data_list[1][1] = np.roll(data_list[1][1], 1)
        data_list[1][1][0] = gyro_data[1]
        data_list[1][2] = np.roll(data_list[1][2], 1)
        data_list[1][2][0] = gyro_data[2]

        # グラフへデータの再セット
        lines[0][0].set_data(sec, data_list[0][0])
        lines[0][1].set_data(sec, data_list[0][1])
        lines[0][2].set_data(sec, data_list[0][2])

        lines[1][0].set_data(sec, data_list[1][0])
        lines[1][1].set_data(sec, data_list[1][1])
        lines[1][2].set_data(sec, data_list[1][2])

        # X軸の更新
        ax[0].set_xlim((sec.min(), sec.max()))
        ax[1].set_xlim((sec.min(), sec.max()))

        plt.pause(0.1)  # sleep時間（秒）

        # print("【加速度】 x:" + accel_data[0], end=" ")
        # print("y:" + accel_data[1], end=" ")
        # print("z:" + accel_data[2], end=" ")
        # print("【角速度】 x:" + gyro_data[0], end=" ")
        # print("y:" + gyro_data[1], end=" ")
        # print("z:" + gyro_data[2])

        return sec, data_list, lines, ax


if __name__ == "__main__":
    main()
