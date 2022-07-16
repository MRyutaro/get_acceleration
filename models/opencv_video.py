import cv2
import datetime


class OpencvVideo(object):
    def __init__(self, video_time=None, video_fps=None):
        print("test_video")
        self.video_time = video_time
        self.video_fps = video_fps

        cap = cv2.VideoCapture(1)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        now = datetime.datetime.today().strftime('%Y_%m%d_%H%M')
        name = "data/" + now + "/video.mp4"
        video = cv2.VideoWriter(name, fourcc, self.video_fps, (width, height))

        print("video_start")
        roop = int(self.video_fps * self.video_time)
        for i in range(roop):
            ret, frame = cap.read()
            video.write(frame)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        print("video_stop")
        video.release()
        cap.release()
        cv2.destroyAllWindows()
