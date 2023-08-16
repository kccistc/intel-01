#!/usr/bin/env python3

# system, 알파벳 순서
import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

# third party
import cv2
import numpy as np
from openvino.inference_engine import IECore
from openvino.runtime import Core, Layout, Type
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm

from iotdemo import FactoryController, MotionDetector, ColorDetector

FORCE_STOP = False


def thread_cam1(q):
    # TODO: MotionDetector
    det = MotionDetector()
    det.load_preset("./motion.cfg", "default")

    # TODO: Load and initialize OpenVINO
    core = Core()
    model_path = "openvino.xml"
    model = core.read_model("openvino.xml")

    # TODO: HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    videoFile = '/home/intel/repo/kcci.intel.ai.project/Class02/smart_factory_src/resources/factory/conveyor.mp4'
    cap = cv2.VideoCapture(videoFile)

    one_flag = True

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live", frame))

        # TODO: Motion detect
        detected = det.detect(frame)
        if detected is None:
            continue

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO:Cam1 detected", detected))

        # abnormal detect
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # reshaped = detected[:, :, [2, 1, 0]]
        # np_data = np.moveaxis(reshaped, -1, 0)
        # preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        # batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # TODO: Inference OpenVINO
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

        if probs[0] >0.0:
            print("NG")
            q.put(("PUSH",1))
        else:
            print("OK")

        # TODO: Calculate ratios
        #print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # TODO: in queue for moving the actuator 1

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector
    det = MotionDetector()
    det.load_preset("motion.cfg", "default")

    # TODO: ColorDetector
    color = ColorDetector()
    color.load_preset("color.cfg", "default")

    # TODO: HW2 Open "resources/factory/conveyor.mp4" video clip
    videoFile = '/home/intel/repo/kcci.intel.ai.project/Class02/smart_factory_src/resources/factory/conveyor.mp4'
    cap = cv2.VideoCapture(videoFile)

    # cap = cv2.VideoCapture("/dev/videoN")

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam2 live", frame))

        # TODO: Detect motion
        detected = det.detect(frame)
        if detected is None :
            continue

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
        q.put(("VIDEO: Cam2 Detected", detected))


        # TODO: Detect color
        predict = color.detect(detected)
        if not  predict:
            continue

        # TODO: Compute ratio
        name , ratio = predict[0]
        ratio *=100
        print(f'{name}: {ratio : .2f}%')

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

    # TODO: HW2 Create a Queue
    q = Queue()

    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q,), daemon=True)
    t2 = threading.Thread(target=thread_cam2, args=(q,), daemon=True)
    
    t1.start()
    print("thread_cam1 start")
    t2.start()
    print("thread_cam2 start")

    
    
    

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data

            try:
                event = q.get_nowait()
            except:
                continue

            name, frm = event

            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            # "VIDEO:Cam1 live"
            # "VIDEO:Cam2 live"
            # "VIDEO:Cam1 detected"
            if name.startswith("VIDEO:"):
                imshow(name[6:], frm)

            # TODO: Control actuator, name == 'PUSH'
            elif name == "PUSH":
                ctrl.push_actuator(frm)

            if name == 'DONE':
                FORCE_STOP = True
                print("Done")   

            q.task_done()

    print("thread_cam1 join")
    print("thread_cam2 join")
    t1.join()
    t2.join()

    cv2.destroyAllWindows()

    


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()


