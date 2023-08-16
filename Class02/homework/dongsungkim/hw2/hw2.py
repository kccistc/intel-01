#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore

from iotdemo import FactoryController

FORCE_STOP = False


def thread_cam1(q):

    cap = cv2.VideoCapture('resources/factory/conveyor.mp4')

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

       
        q.put(("VIDEO:Cam1 live", frame))
        

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
   
    cap = cv2.VideoCapture('resources/factory/conveyor.mp4')

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        q.put(("VIDEO:Cam2 live", frame))


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

    q = Queue()

    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q,))
    t2 = threading.Thread(target=thread_cam2, args=(q,))
    t1.start()
    t2.start()
    
    
    while not FORCE_STOP:
        if cv2.waitKey(10) & 0xff == ord('q'):
            break

        try:
            name, data = q.get_nowait()
            if name == "VIDEO:Cam1 live":
                imshow("Cam1 live", data)
            elif name == "VIDEO:Cam2 live":
                imshow("Cam2 live", data)
            if name == 'PUSH':
                pass
            if name == 'DONE':
                FORCE_STOP = True
            q.task_done()
        except Empty:
            pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
