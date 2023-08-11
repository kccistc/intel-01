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


def thread_cam1(q):
    # MotionDetector
    det = MotionDetector()
    det.load_preset("motion.cfg", "default")
    
    # Load and initialize OpenVINO
    core = Core()
    model = core.read_model("/home/intel/smart_factory_workspace/MobileNet-V3-large-1x-classification/outputs/20230810_182410_export/openvino/openvino.xml")
    # HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture("resources/factory/conveyor.mp4")
#    cap = cv2.VideoCapture("/dev/video2")

    one_flag = True
    
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(('VIDEO:Cam1 live', frame))

        # Motion detect
        detetecd = det.detect(frame)
        if detetecd is None:
            continue

        # nqueue "VIDEO:Cam1 detected", detected info.
        q.put(('VIDEO:Cam1 detected', detetecd))
        
        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      #  reshaped = detected[:, :, [2, 1, 0]]
      #  np_data = np.moveaxis(reshaped, -1, 0)
      #  preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
      #  batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # TODO: Inference OpenVINO
        input_tensor = np.expand_dims(detetecd, 0)
        
        
        if one_flag is True:
            ppp = PrePostProcessor(model)
            ppp.input().tensor() \
            .set_shape(input_tensor.shape) \
            .set_element_type(Type.u8) \
            .set_layout(Layout('NHWC'))
            ppp.input().preprocess().resize(ResizeAlgorithm.RESIZE_LINEAR)
            ppp.input().model().set_layout(Layout('NCHW'))
            ppp.output().tensor().set_element_type(Type.f32)
            
            model = ppp.build()
            compiled_model = core.compile_model(model, "CPU")
            one_flag = False
            
        results = compiled_model.infer_new_request({0: input_tensor})
        predictions = next(iter(results.values()))
        probs = predictions.reshape(-1)
        
        #in queue for moving the actuator 1
        if probs[0] > 0.0:
            print('NG!')
            q.put(('PUSH', 1))
        else:
            print('OK.')

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # MotionDetector
    det = MotionDetector()
    det.load_preset("motion.cfg", "default")
    
    # ColorDetector
    color = ColorDetector()
    color.load_preset("color.cfg", "default")
    
    # HW2 Open "resources/factory/conveyor.mp4" video clip
    cap = cv2.VideoCapture("resources/factory/conveyor.mp4")
#    cap = cv2.VideoCapture("/dev/video4")
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(('VIDEO:Cam2 live', frame))

        # Detect motion
        detetecd = det.detect(frame)
        if detetecd is None:
            continue
        # Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(('VIDEO:Cam2 detected', detetecd))

        # Detect color
        predict = color.detect(detetecd)
        if not predict:
            continue
        
        # Compute ratio
        name, ratio = predict[0]
        ratio *= 100
        print(f"{name}: {ratio: .2f}%")

        # Enqueue to handle actuator 2
        if name == "blue" and ratio > .5:
            q.put(("PUSH", 2))
            
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

    # HW2 Create a Queue
    q = Queue()
    
    # HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q,), daemon=True)
    t2 = threading.Thread(target=thread_cam2, args=(q,), daemon=True)
    
    t1.start()
    t2.start()
    
    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            try:
                event = q.get_nowait()
            except Empty:
                continue
            
            name, data = event
            
            # HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name.startswith("VIDEO:"):
                imshow(name[6:], data)
                
            # Control actuator, name == 'PUSH'
            elif name == "PUSH":
                ctrl.push_actuator(data)
            elif name == 'DONE':
                FORCE_STOP = True

            q.task_done()
            
    t1.join()
    t2.join()
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
 