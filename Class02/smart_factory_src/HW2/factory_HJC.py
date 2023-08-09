#두개의 비디오 입력을 받아들이는 thread thread_cam1, thread_cam2를 구현하고 queue로 live camera frame정보를 전달.
#비디오는 resources/factory/conveyor.mp4에 있음.
#Main thread에서 queue를 검사해서 thread로 부터의 입력이 있으면 각각을 Cam1 live와 Cam2 live 창으로 출력해야 함.


#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Queue
from time import sleep

import cv2

FORCE_STOP = False
CAM1_LIVE_KEY = "VIDEO:Cam1 live"
CAM2_LIVE_KEY = "VIDEO:Cam2 live"
VIDEO_CLIP = "resources/factory/conveyor.mp4"

def thread_cam1(q):
    cap = cv2.VideoCapture(VIDEO_CLIP)
    
    while not FORCE_STOP:
        sleep(0.03)
        ret, frame = cap.read()
        if not ret:
            break
        
        q.put((CAM1_LIVE_KEY, frame))
    
    cap.release()
    q.put(('DONE', None))
    exit()

def thread_cam2(q):
    cap = cv2.VideoCapture(VIDEO_CLIP)
    
    while not FORCE_STOP:
        sleep(0.03)
        ret, frame = cap.read()
        if not ret:
            break
        
        q.put((CAM2_LIVE_KEY, frame))
    
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

    cam1_thread = threading.Thread(target=thread_cam1, args=(q,))
    cam2_thread = threading.Thread(target=thread_cam2, args=(q,))
    
    cam1_thread.start()
    cam2_thread.start()

    while not FORCE_STOP:
        if cv2.waitKey(10) & 0xff == ord('q'):
            break

        try:
            name, frame = q.get(timeout=0.1)
        except Empty:
            continue

        if name == 'DONE':
            FORCE_STOP = True
            continue

        if name == CAM1_LIVE_KEY:
            imshow('Cam1 live', frame)
        elif name == CAM2_LIVE_KEY:
            imshow('Cam2 live', frame)

        q.task_done()

    q.join()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        FORCE_STOP = True
