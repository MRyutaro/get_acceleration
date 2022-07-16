import cv2
import datetime

time = 5

fps = 30.0
cap = cv2.VideoCapture(1)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
now = datetime.datetime.today().strftime('%Y_%m%d_%H%M')
name = "data/video/" + now + ".mp4"
video = cv2.VideoWriter(name, fourcc, fps, (width, height))

print("start")
roop = int(fps * time)
for i in range(roop):
    ret, frame = cap.read()
    video.write(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

print("stop")
video.release()
cap.release()
cv2.destroyAllWindows()
