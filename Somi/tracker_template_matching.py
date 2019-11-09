import sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from enum import Enum

class TrackingMode(Enum):
    TEMPLATE_MATCHING = 1
    TRACKING = 2

class CustomTracker(object):

    def __init__(self, template, method, tracker):
        self.mode = TrackingMode.TEMPLATE_MATCHING
        self.template = template
        self.method = method
        self.tracker = tracker

    def processReinit(self, frame):
        res = cv.matchTemplate(frame, self.template, self.method)

        w, h = self.template.shape[0:2][::-1]

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        box = (max_loc[0], max_loc[1], w, h)

        self.tracker.init(frame, box)
        self.mode = TrackingMode.TRACKING

        return box

    def process(self, frame):
        if self.mode == TrackingMode.TRACKING:
            (success, box) = self.tracker.update(frame)
            if success:
                print(box)
                return box
            else:
                self.mode == TrackingMode.TEMPLATE_MATCHING
        # Failed to track
        print("Failed to track, reinitializing")
        return self.processReinit(frame)


def main(args):
    tracker = CustomTracker(cv.imread('red.jpg'), cv.TM_CCOEFF_NORMED, cv.TrackerCSRT_create())

    cap = cv.VideoCapture('test480.mp4')

    i = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if i % 100 == 0:
            print("Reinitializing 1/100 frames")
            (x, y, w, h) = [int(v) for v in tracker.processReinit(frame)]
        else:
            (x, y, w, h) = [int(v) for v in tracker.process(frame)]
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print((x, y, w, h))

        cv.imshow("temp", frame);
        cv.waitKey(100)

        i += 1

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
