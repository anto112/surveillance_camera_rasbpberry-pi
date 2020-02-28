import cv2
# from imutils.video.pivideostream import PiVideoStream
from imutils.video import VideoStream
import imutils
import os
import time
import numpy as np
import datetime

classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")  # an opencv classifier


class VideoCamera(object):
    def __init__(self, flip=False):
        # self.vs = PiVideoStream().start()
        self.vs = VideoStream(src=0).start()
        # self.vs = cv2.VideoCapture(0)
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()
        # self.video.release()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read())
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (14, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # print(objects)
        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if len(objects) > 0:
            found_objects = True
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), found_objects

    def get_image(self, file_name):
        frame = self.flip_if_needed(self.vs.read())
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (14, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # print(objects)
        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite(file_name + ".jpeg", frame)
        # print(frame)
        return frame, file_name
