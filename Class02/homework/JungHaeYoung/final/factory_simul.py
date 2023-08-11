#!/usr/bin/env python3
# %%
import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore
from openvino.runtime import Core, Layout, Type
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm


from iotdemo import FactoryController
from iotdemo import MotionDetector, ColorDetector

FORCE_STOP = False


def thread_cam1(q):
    # MotionDetector
    det = MotionDetector()
    det.load_preset("motion.cfg", "default")
    
    # Load and initialize OpenVINO
    core = Core()
    model_path = "model/EfficientNet-B0/openvino.xml"
    model = core.read_model(model_path)


    #  HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    video_path = 'resources/factory/conveyor.mp4'  # 비디오 파일 경로
    cap = cv2.VideoCapture(video_path)

    one_flag = True

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live",frame))

        # TODO: Motion detect
        detected = det.detect(frame)
        if detected is None :
            continue

        #  Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO: Cam1 Detected", detected))
        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # reshaped = detected[:, :, [2, 1, 0]]
        # np_data = np.moveaxis(reshaped, -1, 0)
        # preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        # batch_tensor = np.stack(preprocessed_numpy, axis=0)

        #  Inference OpenVINO

        input_tensor = np.expand_dims(detected,0)

        if one_flag is True:
            ppp = PrePostProcessor(model)
            ppp.input().tensor() \
                .set_shape(input_tensor.shape) \
                .set_element_type(Type.u8) \
                .set_layout(Layout('NHWC'))  # noqa: ECE001, N400
            ppp.input().preprocess().resize(ResizeAlgorithm.RESIZE_LINEAR)
            ppp.input().model().set_layout(Layout('NCHW'))
            ppp.output().tensor().set_element_type(Type.f32)
            model = ppp.build()
            compiled_model = core.compile_model(model, "CPU")

            one_flag = False

        results = compiled_model.infer_new_request({0: input_tensor})
        predictions = next(iter(results.values()))
        probs = predictions.reshape(-1)

        print(f'{probs}')

        if probs[0] <0.0:
            print("NG")
            q.put(("PUSH",1))
        else:
            print("OK")

        # TODO: Calculate ratios
        # print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # TODO: in queue for moving the actuator 1

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
    video_path = 'resources/factory/conveyor.mp4'  # 비디오 파일 경로
    cap = cv2.VideoCapture(video_path)

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam2 live",frame))
        # Detect motion
        detected = det.detect(frame)
        if detected is None :
            continue

        # Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO: Cam2 Detected", detected))

        # TODO: Detect color
        predict = color.detect(detected)
        if not  predict:
            continue

        # TODO: Compute ratio
        name , ratio = predict[0]
        ratio *=100
        print(f'{name}: {ratio : .2f}%')

        # print(f"{name}: {ratio:.2f}%")

        # TODO: Enqueue to handle actuator 2
        if name =="blue" and ratio > .5:
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
    q= Queue()

    # HW2 Create thread_cam1 and thread_cam2 threads and start them.
    thread1 = threading.Thread(target=thread_cam1, args= (q,), daemon= True)
    thread2 = threading.Thread(target=thread_cam2, args= (q,), daemon= True)

    thread1.start()
    thread2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            try: 
               event = q.get_nowait()          
               #event = q.get_nowait()
            except Empty:                
               continue
            name, data = event
            # HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            # if name == "VIDEO:Cam1 live":
            #     imshow(name,data, pos=(0,0))
            # elif name == "VIDEO:Cam2 live":
            #     imshow(name,data, pos=(640,0))                 

            if name.startswith("VIDEO:"):
                imshow(name[6:],data)

            # Control actuator, name == 'PUSH'
            elif name == "PUSH":
                ctrl.push_actuator(data)

            elif name == 'DONE':
                FORCE_STOP = True   
                print("Done")   

            q.task_done()

    thread1.join()
    thread2.join()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()

# %%
