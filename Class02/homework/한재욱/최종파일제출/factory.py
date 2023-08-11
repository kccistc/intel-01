#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm
from openvino.runtime import Core, Layout, Type
from openvino.inference_engine import IECore

from iotdemo import FactoryController, MotionDetector, ColorDetector

FORCE_STOP = False


def thread_cam1(q): #cam1, cam2 shared 
    # TODO: MotionDetector
    det = MotionDetector()
    det.load_preset("resources/factory/motion.cfg","default")
    # TODO: Load and initialize OpenVINO

    model_path="resources/factory/model.xml"
    core = Core()
    model = core.read_model(model_path)
    
    # TODO: HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture("resources/factory/conveyor.mp4")

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            print("bbbbb")
            break

        #HW2 Enqueue "VIDEO:Cam1 live", frame info
        name = "VIDEO:Cam1 live"
        q.put((name,frame))

        # TODO: Motion detect
        detected = det.detect(frame)
        if detected is None:
            continue

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO:Cam1 live detected",detected))

        # abnormal detect
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #reshaped = detected[:, :, [2, 1, 0]]
        #np_data = np.moveaxis(reshaped, -1, 0)
        #preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        #batch_tensor = np.stack(preprocessed_numpy, axis=0)
#
        # TODO: Inference OpenVINO

        # TODO: Calculate ratios
        #print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # TODO: in queue for moving the actuator 1

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetectorreshaped = detected
    det = MotionDetector()
    det.load_preset("resources/factory/motion.cfg","default")
    cap = cv2.VideoCapture("resources/factory/conveyor.mp4")
    
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            print("bbbbb")
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        name = "VIDEO:Cam2 live"
        q.put((name,frame))
        
        

        # TODO: Detect motion
        detected = det.detect(frame)
        if detected is None:
            continue


        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO:Cam2 live detected",detected))
        
        # TODO: Detect color
        color = ColorDetector()
        color.load_preset("resources/factory/color.cfg","default")
        predict = color.detect(detected)
        if not predict:
            continue

        # TODO: Compute ratio
        name, ratio =predict[0]
        ratio*= 100
        print(f"{name}: {ratio:.2f}%")

        # TODO: Enqueue to handle actuator 2
        if name == "blue" and ratio > .5:
            q.put("PUSH",2)
        
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

    #HW2 Create a Queue
    q = Queue() 
    
    
    #HW2 Create thread_cam1 and thread_cam2 threads and start them.
    cam1_thread = threading.Thread(target=thread_cam1, args=(q,),daemon=True)
    cam2_thread = threading.Thread(target=thread_cam2, args=(q,),daemon=True)
    cam1_thread.start()
    cam2_thread.start()
    
    

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            try:
                q.get_nowait()
            except Empty:
                continue
            data = q.get()
            name = data[0]
            frame = data[1]
         
         
            if name == "VIDEO:Cam1 live":
                imshow(name, frame)
            elif name == "VIDEO:Cam2 live":
                imshow(name, frame)
            elif name == "PUSH":
                ctrl.push()
            elif name == "DONE":
                FORCE_STOP = True
            
            
            # de-queue name and data
           
           

            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name.startswith("VIDEO:"):
                imshow(name[6:], frame)
        
            # TODO: Control actuator, name == 'PUSH'
            elif name == 'PUSH':
                ctrl.push_actuator(data)
            elif name == 'DONE':
                FORCE_STOP = True
            else:
                pass

            q.task_done()

    cv2.destroyAllWindows()
    cam1_thread.join()
    cam2_thread.join()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()