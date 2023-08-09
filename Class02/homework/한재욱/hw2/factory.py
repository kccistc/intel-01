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
    # TODO: MotionDetector
    from iotdemo import MotionDetector
    motion_detector = MotionDetector()

    # TODO: ColorDetector
    from iotdemo import ColorDetector
    color_detector = ColorDetector()

    # TODO: HW2 Open "resources/factory/conveyor.mp4" video clip
    cap = cv2.VideoCapture("resources/factory/conveyor.mp4")

    while not FORCE_STOP:
        sleep(0.03)
        ret, frame = cap.read()
        if not ret:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live", frame))

        # TODO: Detect motion
        motion_detected = motion_detector.detect(frame)  # Change this line
        if motion_detected:
            # TODO: Enqueue "VIDEO:Cam1 detected", detected info.
            q.put(("VIDEO:Cam1 detected", motion_detected))

            # TODO: Detect color
            color_name, ratio = color_detector.detect_color(frame)  # Change this line
            print(f"{color_name}: {ratio:.2f}%")

            # TODO: Enqueue to handle actuator 1
            q.put(("PUSH", {'color_name': color_name, 'ratio': ratio}))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector
    from iotdemo import MotionDetector
    motion_detector = MotionDetector()

    # TODO: ColorDetector
    from iotdemo import ColorDetector
    color_detector = ColorDetector()

    # TODO: HW2 Open "resources/factory/conveyor.mp4" video clip
    cap = cv2.VideoCapture("resources/factory/conveyor1.mp4")

    while not FORCE_STOP:
        sleep(0.03)
        ret, frame = cap.read()
        if not ret:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam2 live", frame))

        # TODO: Detect motion
        motion_detected = motion_detector.detect(frame)  # Change this line
        if motion_detected:
            # TODO: Enqueue "VIDEO:Cam2 detected", detected info.
            q.put(("VIDEO:Cam2 detected", motion_detected))

            # TODO: Detect color
            color_name, ratio = color_detector.detect_color(frame)  # Change this line
            print(f"{color_name}: {ratio:.2f}%")

            # TODO: Enqueue to handle actuator 2
            q.put(("PUSH", {'color_name': color_name, 'ratio': ratio}))

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
    t_cam1 = threading.Thread(target=thread_cam1, args=(q,))
    t_cam2 = threading.Thread(target=thread_cam2, args=(q,))
    t_cam1.start()
    t_cam2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            try:
                # TODO: HW2 Get an item from the queue. You might need to properly handle exceptions.
                name, data = q.get(timeout=0.1)
            except Empty:
                continue

            # TODO: HW2 Show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            imshow(name, data)

            # TODO: Control actuator, name == 'PUSH'
            if name == 'PUSH':
                if 'x_ratio' in data and 'circle_ratio' in data:
                    ctrl.move_actuator1(data['x_ratio'], data['circle_ratio'])
                elif 'color_name' in data and 'ratio' in data:
                    ctrl.move_actuator2(data['color_name'], data['ratio'])

            if name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()