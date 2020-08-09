#!ve/bin/python3

import boto3
import cv2
import logging
import time
from botocore.exceptions import ClientError
from datetime import datetime
from io import BytesIO

INTERVAL = 1
BUCKET = "thraxil-veilig"
DEV_IDX = 0  # video capture device index
MOTION_THRESHOLD = 200
STATIC_UPLOAD_INTERVAL = 60


def upload_file(f, bucket, object_name=None):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(f, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


prev = None

cnt = 0
while True:
    webcam = cv2.VideoCapture(DEV_IDX)
    ret, video_frame = webcam.read()
    webcam.release()

    gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    motion = False
    if prev is not None:
        frameDelta = cv2.absdiff(prev, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < MOTION_THRESHOLD:
                continue
            # (x, y, w, h) = cv2.boundingRect(c)
            # rect = cv2.rectangle(video_frame, (x, y),
            #                      (x + w, y + h), (0, 255, 0), 2)
            motion = True
            # cv2.imwrite('countour.jpg', rect)
    n = datetime.utcnow()
    fname = (f"{n.year}-{n.month:02}-{n.day:02}/"
             f"{n.hour:02}-{n.minute:02}-{n.second:02}.jpg")
    print(fname, motion)
    _, im_jpg = cv2.imencode('.jpg', video_frame)
    b = BytesIO(im_jpg)
    if motion or (cnt % STATIC_UPLOAD_INTERVAL) == 0:
        # upload the image if there's motion
        # or every so often even if static
        upload_file(b, BUCKET, object_name=fname)
    prev = gray
    cnt += 1
    time.sleep(INTERVAL)
