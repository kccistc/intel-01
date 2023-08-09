#!/usr/bin/env python3

import os
import threading
from time import sleep

import cv2
from queue import Queue
FORCE_STOP = False
CAM1_LIVE_KEY = "VIDEO:Cam1 live"
CAM2_LIVE_KEY = "VIDEO:Cam2 live"
VIDEO_CLIP = 'resources/factory/conveyor.mp4'
WIN_CAM1_LIVE = 'Cam1 live'
WIN_CAM2_LIVE = 'Cam2 live'


def thread_cam1(q):
    # TODO: MotionDetector

    # TODO: Load and initialize OpenVINO

    # TODO: HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    
    cap = cv2.VideoCapture(VIDEO_CLIP)
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put((CAM1_LIVE_KEY,frame))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector

    # TODO: Load and initialize OpenVINO

    # TODO: HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    
    cap = cv2.VideoCapture(VIDEO_CLIP)
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put((CAM2_LIVE_KEY,frame))

    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    global FORCE_STOP

    # TODO: HW2 Create a Queue
    q = Queue()
    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    capture_thread1 = threading.Thread(target=thread_cam1, args=[q])
    capture_thread2 = threading.Thread(target=thread_cam2, args=[q])
    capture_thread1.start()
    capture_thread2.start()
    while not FORCE_STOP:
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
        
        # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
        # de-queue name and data
        if q.empty():
            continue
        msg = q.get()
        name, frame = msg
        # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
        if name == CAM1_LIVE_KEY:
            imshow(WIN_CAM1_LIVE, frame)
        elif name == CAM2_LIVE_KEY:
            imshow(WIN_CAM2_LIVE, frame)
        elif name == 'DONE':
            FORCE_STOP = True
        else:
            pass
        q.task_done()

    cv2.destroyAllWindows()
    capture_thread1.join()
    capture_thread2.join()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
