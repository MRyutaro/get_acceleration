import matplotlib.pyplot as plt
import numpy as np
import serial


def plot_loop():
    # データの取得
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    line = ser.readline()
    line_disp = line.strip().decode('UTF-8')
    line_disp = line_disp.split(',')

    # センサーデータ取得
    accel_data = [0]*3
    gyro_data = [0]*3
    if len(line_disp) == 7:
        accel_data = [line_disp[0], line_disp[1], line_disp[2]]
        gyro_data = [line_disp[3], line_disp[4], line_disp[5]]

    fig, (ax_accel, ax_gyro) = plt.subplots(ncols=2, figsize=(6, 4))

    # X座標
    sec = np.arange(-np.pi, np.pi, 0.1)

    # 加速度のY座標
    # ロール軸(x)
    accel_list_x = np.zeros(63)
    accel_list_x[0] = accel_data[0]
    accel_x_lines, = ax_accel.plot(sec, accel_list_x, color="red", label="x")

    # ピッチ軸(y)
    accel_list_y = np.zeros(63)
    accel_list_y[0] = accel_data[1]
    accel_y_lines, = ax_accel.plot(sec, accel_list_y, color="blue", label="y")

    # ヨー軸(z)
    accel_list_z = np.zeros(63)
    accel_list_z[0] = accel_data[2]
    accel_z_lines, = ax_accel.plot(sec, accel_list_z, color="green", label="z")

    ax_accel.legend()  # ラベル描画
    ax_accel.set_title("accel")
    ax_accel.set_ylim(-4, 4)
    ax_accel.set_xticks([])  # X軸のメモリ非表示

    # 角速度のY座標
    # ロール軸(x)
    gyro_list_x = np.zeros(63)
    gyro_list_x[0] = gyro_data[0]
    gyro_x_lines, = ax_gyro.plot(sec, gyro_list_x, color="red", label="x")

    # ピッチ軸(y)
    gyro_list_y = np.zeros(63)
    gyro_list_y[0] = gyro_data[1]
    gyro_y_lines, = ax_gyro.plot(sec, gyro_list_y, color="blue", label="y")

    # ヨー軸(z)
    gyro_list_z = np.zeros(63)
    gyro_list_z[0] = gyro_data[2]
    gyro_z_lines, = ax_gyro.plot(sec, gyro_list_z, color="green", label="z")

    ax_gyro.legend()  # ラベル描画
    ax_gyro.set_title("gyro")
    ax_gyro.set_ylim(-300, 300)
    ax_gyro.set_xticks([])  # X軸のメモリ非表示

    # plotし続ける
    while True:
        line = ser.readline()
        line_disp = line.strip().decode('UTF-8')
        line_disp = line_disp.split(',')
        if len(line_disp) != 7:
            continue

        # センサーデータ取得
        accel_data = [line_disp[0], line_disp[1], line_disp[2]]
        gyro_data = [line_disp[3], line_disp[4], line_disp[5]]

        # データの更新
        sec += 0.1

        accel_list_x = np.roll(accel_list_x, 1)
        accel_list_x[0] = accel_data[0]
        accel_list_y = np.roll(accel_list_y, 1)
        accel_list_y[0] = accel_data[1]
        accel_list_z = np.roll(accel_list_z, 1)
        accel_list_z[0] = accel_data[2]

        gyro_list_x = np.roll(gyro_list_x, 1)
        gyro_list_x[0] = gyro_data[0]
        gyro_list_y = np.roll(gyro_list_y, 1)
        gyro_list_y[0] = gyro_data[1]
        gyro_list_z = np.roll(gyro_list_z, 1)
        gyro_list_z[0] = gyro_data[2]

        # グラフへデータの再セット
        accel_x_lines.set_data(sec, accel_list_x)
        accel_y_lines.set_data(sec, accel_list_y)
        accel_z_lines.set_data(sec, accel_list_z)

        gyro_x_lines.set_data(sec, gyro_list_x)
        gyro_y_lines.set_data(sec, gyro_list_y)
        gyro_z_lines.set_data(sec, gyro_list_z)

        # X軸の更新
        ax_accel.set_xlim((sec.min(), sec.max()))
        ax_gyro.set_xlim((sec.min(), sec.max()))

        print("【加速度】 x:" + accel_data[0], end=" ")
        print("y:" + accel_data[1], end=" ")
        print("z:" + accel_data[2], end=" ")
        print("【角速度】 x:" + gyro_data[0], end=" ")
        print("y:" + gyro_data[1], end=" ")
        print("z:" + gyro_data[2])

        plt.pause(0.1)  # sleep時間（秒）


if __name__ == "__main__":
    plot_loop()
