import glob
import os
import shutil
import toml


def move_and_rename_video():
    obj = toml.load("settings.toml")
    VIDEO_DIR = obj["video_settings"]["VIDEO_DIR"]
    # print(VIDEO_DIR)

    for file in glob.glob(VIDEO_DIR + "/*.mp4"):
        shutil.move(file, "./data")
        no_file = file[39:53].replace("_", "")
        new_file_name = no_file[:4] + "_" + no_file[4:8] + "_" + no_file[8:12]
        old_file_name = file[35:]
        old_file_path = "data/" + old_file_name
        new_file_path = "data/" + new_file_name + ".mp4"
        os.rename(old_file_path, new_file_path)


if __name__ == "__main__":
    move_and_rename_video()
