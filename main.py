import datetime
import toml
import os
from models.opencv_video import OpencvVideo as OV
from models.data_acquisition import DataAcquisition as DA


def make_dir():
    now = datetime.datetime.today().strftime('%Y_%m%d_%H%M')
    path = "data/" + now
    if os.path.exists(path) is True:
        print("1分後待ってプログラムを動かしてください\n")
        exit()
    os.mkdir(path)


if __name__ == "__main__":
    obj = toml.load("settings.toml")
    video_time = obj["settings"]["video_time"]
    fps = obj["settings"]["video_fps"]

    make_dir()

    OV(video_time, fps)
    DA()
