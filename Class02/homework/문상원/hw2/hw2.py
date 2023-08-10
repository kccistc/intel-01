#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
#from openvino.inference_engine import IECore

from iotdemo import FactoryController

FORCE_STOP = False


def thread_cam1(q):
    # TODO: MotionDetector

    # TODO: Load and initialize OpenVINO
    # TODO: HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    # 프레임당 정보 얻기 (opencv 사용)
    filePath="./resources/factory/conveyor.mp4"
    cap = cv2.VideoCapture(filePath)

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        # q.put({"VIDEO:Cam1 live": frame}) X
        # imshow("VIDEO:Cam1 live", frame)
        q.put({"VIDEO:Cam1 live": frame})
        # TODO: Motion detect

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.

        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #reshaped = detected[:, :, [2, 1, 0]]
        #np_data = np.moveaxis(reshaped, -1, 0)
        #preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        #batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # TODO: Inference OpenVINO

        # TODO: Calculate ratios
        #print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # TODO: in queue for moving the actuator 1

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector

    # TODO: ColorDetector
    # TODO: HW2 Open "resources/factory/conveyor.mp4" video clip
    filePath="./resources/factory/conveyor.mp4"
    cap = cv2.VideoCapture(filePath)
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        # q.put({"VIDEO:Cam2 live": frame})
        q.put({"VIDEO:Cam2 live": frame})
        # TODO: Detect motion

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.

        # TODO: Detect color

        # TODO: Compute ratio
        #print(f"{name}: {ratio:.2f}%")

        # TODO: Enqueue to handle actuator 2

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

    parser = ArgumentParser(prog='python3 factory1.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # TODO: HW2 Create a Queue
    # data = q.모종의 방법() 처럼 생성
    q = Queue() 
    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q,))
    t2 = threading.Thread(target=thread_cam2, args=(q,))

    t1.start()
    t2.start()


    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break
            name =''
            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            # q를 모종의 방법으로 까서 VIDEO:Cam1 live 인지 VIDEO:Cam2 live 인지 체크해서 해당 타이틀로 imshow
            try:
                item = q.get(timeout=1)  
                if isinstance(item, dict):  
                    name, data = list(item.keys())[0], list(item.values())[0]
                else:
                    break  
            except Empty:
                continue  

            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name == 'VIDEO:Cam1 live' or name == 'VIDEO:Cam2 live':
                imshow(name, data)

            # TODO: Control actuator, name == 'PUSH'

            if name == 'DONE':
                FORCE_STOP = True
                

            q.task_done()
            
    cv2.destroyAllWindows()
    t1.join()
    t2.join()
    


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
