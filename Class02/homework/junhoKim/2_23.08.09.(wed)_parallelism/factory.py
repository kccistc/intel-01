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

THEARD1_QUEUE_NAME = "VIDEO:Cam1 live"
THEARD2_QUEUE_NAME = "VIDEO:Cam2 live"
FILE = "./resources/factory/conveyor.mp4"

def thread_cam1(q):
    cap = cv2.VideoCapture(FILE)
    
    if not cap.isOpened():
        print("Camera open failed!") # 열리지 않았으면 문자열 출력

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break
        q.put((THEARD1_QUEUE_NAME, frame))

    cap.release()
    exit()

def thread_cam2(q):
    cap = cv2.VideoCapture(FILE)
    if not cap.isOpened():
        print("Camera open failed!") # 열리지 않았으면 문자열 출력

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        q.put((THEARD2_QUEUE_NAME, frame))

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

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    q = Queue()

    t1 = threading.Thread(target=thread_cam1, args=[q,])
    t2 = threading.Thread(target=thread_cam2, args=[q,])
    t1.start()
    t2.start()
    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                t1.join()
                t2.join()
                break

            name, frame = q.get()

            if name == THEARD1_QUEUE_NAME:
                imshow("Cam1 live", frame)
            if name == THEARD2_QUEUE_NAME:
                imshow("Cam2 live", frame)

            if name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
