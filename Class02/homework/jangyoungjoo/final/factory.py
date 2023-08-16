#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm
from openvino.runtime import Core, Layout, Type

from iotdemo import FactoryController, MotionDetector, ColorDetector

FORCE_STOP = False
CAM1_LIVE_KEY = "VIDEO:Cam1 live"
CAM2_LIVE_KEY = "VIDEO:Cam2 live"
CAM1_DET_KEY = "VIDEO:Cam1 detected"
CAM2_DET_KEY = "VIDEO:Cam2 detected"
VIDEO_CLIP = 'resources/factory/conveyor.mp4'
WIN_CAM1_LIVE = 'Cam1 live'
WIN_CAM2_LIVE = 'Cam2 live'
MOTION_CFG_PATH = 'motion.cfg'
COLOR_CFG_PATH = 'color.cfg'


def thread_cam1(q):
    # MotionDetector
    det = MotionDetector()
    det.load_preset(MOTION_CFG_PATH, 'default')
    # Load and initialize OpenVINO
    core = Core()
    model = core.read_model('../homework/jangyoungjoo/hw3/export-EfficientNet-B0/openvino.xml')

    # HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture(VIDEO_CLIP)
    #cap = cv2.VideoCapture('/dev/video2')

    one_flag = True



    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put((CAM1_LIVE_KEY,frame))
        # Motion detect
        detected = det.detect(frame)
        if detected is None:
            continue
        # Enqueue "VIDEO:Cam1 detected", detected info.
        q.put((CAM1_DET_KEY, detected))
        input_tensor = np.expand_dims(detected, 0)
        if one_flag:
            ppp = PrePostProcessor(model)
            ppp.input().tensor() \
                .set_shape(input_tensor.shape) \
                .set_element_type(Type.u8) \
                .set_layout(Layout('NHWC'))  # noqa: ECE001, N400
            ppp.input().preprocess().resize(ResizeAlgorithm.RESIZE_LINEAR)

            ppp.input().model().set_layout(Layout('NCHW'))
            ppp.output().tensor().set_element_type(Type.f32)
            model = ppp.build()
            compiled_model = core.compile_model(model, 'CPU')
            one_flag = False
        results = compiled_model.infer_new_request({0: input_tensor})
        predictions = next(iter(results.values()))
        probs = predictions.reshape(-1)
       
        if probs[0] > 0.:
            q.put(('PUSH', 1))
            print('ng', probs)
        else:
            print('ok',probs)

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # MotionDetector
    det = MotionDetector()
    det.load_preset(MOTION_CFG_PATH, 'default')
    # ColorDetector
    color = ColorDetector()
    color.load_preset(COLOR_CFG_PATH, 'default')
    # HW2 Open "resources/factory/conveyor.mp4" video clip
    cap = cv2.VideoCapture(VIDEO_CLIP)
    #cap = cv2.VideoCapture('/dev/video4')
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put((CAM2_LIVE_KEY,frame))
        # Detect motion
        # Motion detect
        detected = det.detect(frame)
        if detected is None:
            continue
        # Enqueue "VIDEO:Cam1 detected", detected info.
        q.put((CAM2_DET_KEY, detected))
        # Detect color
        predict = color.detect(detected)
        if predict is None:
            continue
        # Compute ratio
        name, ratio = predict[0]
        ratio *= 100
        #print(f'{name} : {ratio: .2f}%')
        # Enqueue to handle actuator 2
        if name == 'blue' and ratio > 0.5:
            q.put(('PUSH',2))

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

    # Create a Queue
    q = Queue()
    # Create thread_cam1 and thread_cam2 threads and start them.
    capture_thread1 = threading.Thread(target=thread_cam1, args=[q], daemon=True)
    capture_thread2 = threading.Thread(target=thread_cam2, args=[q], daemon=True)
    capture_thread1.start()
    capture_thread2.start()
    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            if q.empty():
                continue
            msg = q.get()
            name, data = msg

            if name.startswith('VIDEO:'):
                imshow(name[6:], data)
            elif name == 'PUSH':
                ctrl.push_actuator(data)
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
