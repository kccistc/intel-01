from time import sleep

import cv2
from PyQt5 import QtCore

__all__ = ('VideoThread', )


class VideoThread(QtCore.QThread):
    frame = QtCore.pyqtSignal(object)

    def __init__(self, device, parent=None, *, fps=None):
        super(VideoThread, self).__init__(parent=parent)
        self.started = False
        self.fps = fps
        self.cam = cv2.VideoCapture(device)

        ret, frame = self.cam.read()
        if not ret:
            raise Exception('Unable to read frame')

        self.height, self.width, *_ = frame.shape

    def __del__(self):
        self.stop()

    def run(self):
        fps = self.fps

        self.setTerminationEnabled(True)
        self.started = True
        while self.started:
            _, frame = self.cam.read()
            if frame is None:
                if fps:
                    self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            self.frame.emit(frame)
            if fps:
                sleep(fps)

    def stop(self):
        self.started = False
        if self.cam:
            self.cam.release()
            self.cam = None
