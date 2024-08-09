import cv2
import time
import numpy as np
from datetime import datetime
from threading import Thread, Lock, Condition
import time
from Queue import Queue

class WebcamVideoStream:

    def __init__(self, src=0):
        # initialize the video camera stream 
        self.stream = cv2.VideoCapture(src)
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.frame = None

    def start(self):
        global qt
        self.stopped = False
        qt = Queue(10)
        # start the thread to read frames from the video stream
        thread1 = Thread(target=self.update, args=())
        thread1.start()
        return self

    def update(self):
        global qt
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                return
            _, self.frame = self.stream.read()
            qt.put(self.frame)

    def read(self):
        global qt
        if(not qt.empty()):
            self.CurrFrame=qt.get()
            if self.CurrFrame is not None:
                return self.CurrFrame
        if self.stopped:
            return

    def stop(self):
        print('Stop')
        # indicate that the thread should be stopped
        self.stopped = True
        return self

vs = WebcamVideoStream(src=-1).start()
time.sleep(1)

i = 0
t0 = time.time()
while i < 100:
    frame = vs.read()
while frame is None:
    frame = vs.read()
i = i + 1

rate = 100/(time.time()-t0)
print(rate)

cv2.destroyAllWindows()
vs.stop()