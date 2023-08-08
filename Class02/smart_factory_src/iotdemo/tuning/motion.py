#!/usr/bin/env python3

import logging
import os.path
from argparse import ArgumentParser
from functools import partial
from os import makedirs
from os.path import exists
from time import time

import cv2
from iotdemo.motion.motion_detector import MotionDetector


def _to_point_tuple_(value):
    x1, y1, x2, y2 = value
    return (x1, y1), (x2, y2)


def _to_point_list_(value):
    (x1, y1), (x2, y2) = value
    return [x1, y1, x2, y2]


class VideoFrame:
    MAIN_WINDOW = 'Input'
    ROI_WINDOW = 'Select ROI'
    TUNING_WINDOW = 'Threshold'
    SKIP_TIME_TRACKBAR = 'Skip Time'
    THRESHOLD_TRACKBAR = 'Threshold'
    TOP_RATIO_TRACKBAR = 'Top Ratio'
    MID_RATIO_TRACKBAR = 'Mid Ratio'

    def __init__(self, src, crop, args):
        # Frame source
        self.cap = cv2.VideoCapture(src)
        self.is_live = self.cap.getBackendName() in {'V4L2', 'DSHOW', 'MSMF'}
        self.paused = False
        self.inverted = args.invert

        # Detector
        self.motion = MotionDetector(debug=args.debug)
        if args.loadpreset:
            self.motion.load_preset(args.loadpreset, 'default')
        else:
            self.motion.load_preset(default=True)
            self.motion.set_crop_box((0, 0), crop)
            self.motion.set_inverted(args.invert)
            self.motion.set_flipped(args.flip)

        self.save_preset = partial(self.motion.save_preset, args.preset,
                                   args.key)

        # Internal variables
        self.actions = {}

        self.x = self.y = 0  # ROI select window mouse position

        self.crop_box_pos = _to_point_list_(self.motion.crop_box)
        self.crop_w, self.crop_h = crop
        self.crop_box_pos[1] += self.motion.top_margin
        self.crop_box_pos[3] += self.motion.top_margin
        self.motion.set_crop_box(*_to_point_tuple_(self.crop_box_pos))

        self.roi_opened = 0
        self.rel_roi_box_pos = [0, 0, -1, -1]
        self.__init_default_rel_roi_box_pos()
        self.motion.set_roi_box(*_to_point_tuple_(self.roi_box_pos))

        self.read()
        self.h, self.w, *_ = self.frame.shape

    def __init_default_rel_roi_box_pos(self):
        (x1, y1), (x2, y2) = self.motion.roi_box
        w, h = x2 - x1, y2 - y1

        #cw = int(self.crop_w / 2)
        #cw += int((self.crop_w - w) / 2)
        #ch = int(self.crop_h / 2)
        #ch -= self.motion.top_margin

        cw = int(self.crop_w / 2)
        cw += int((self.crop_w - w) / 2)
        ch = int(self.crop_h / 2)
        ch += int((self.crop_h - h) / 2)

        self.rel_roi_box_pos = [cw, ch, w, h]  # crop_rel_x, crop_rel_y, w, h

    @property
    def roi_box_pos(self):
        rx, ry, w, h = self.rel_roi_box_pos
        dx = rx - int(self.crop_w / 2)
        dy = ry - int(self.crop_h / 2)

        cx, cy, *_ = self.crop_box_pos
        x1, y1 = cx + dx, cy + dy

        return [x1, y1, x1 + w, y1 + h]

    def __del__(self):
        self.close()

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.cap:
            self.cap.release()

        self.cap = None

        if self.motion.changed:
            self.save_preset()

        return False

    def setup(self):
        def _wrapper(idx, val):
            def _set():
                self.rel_roi_box_pos[idx] += val
                if not self.roi_opened:
                    return

                cv2.setTrackbarPos("Y" if idx else "X", VideoFrame.ROI_WINDOW,
                                   self.rel_roi_box_pos[idx])

            return _set

        # Shortcut map
        self.actions = {
            ord('q'): self.close,
            ord(' '): self._space_event,
            ord("r"): self.select_roi,
            81: _wrapper(0, -1),
            82: _wrapper(1, -1),
            83: _wrapper(0, 1),
            84: _wrapper(1, 1),
        }

        # Initialize windows
        cv2.namedWindow(VideoFrame.MAIN_WINDOW)
        cv2.namedWindow(VideoFrame.TUNING_WINDOW)

        cv2.createTrackbar(VideoFrame.SKIP_TIME_TRACKBAR,
                           VideoFrame.TUNING_WINDOW,
                           int(self.motion.skip_time * 1000), 3000,
                           self._skip_time_callback)
        cv2.createTrackbar(VideoFrame.THRESHOLD_TRACKBAR,
                           VideoFrame.TUNING_WINDOW, self.motion.threshold,
                           255, self._threshold_callback)
        cv2.createTrackbar(VideoFrame.TOP_RATIO_TRACKBAR,
                           VideoFrame.TUNING_WINDOW,
                           int(self.motion.top_ratio * 1000), 1000,
                           self._top_ratio_callback)
        cv2.createTrackbar(VideoFrame.MID_RATIO_TRACKBAR,
                           VideoFrame.TUNING_WINDOW,
                           int(self.motion.mid_ratio * 1000), 1000,
                           self._mid_ratio_callback)

        cv2.moveWindow(VideoFrame.MAIN_WINDOW, 100, 100)
        cv2.moveWindow(VideoFrame.TUNING_WINDOW, 800, 125)

    def shortcut(self, key: int):
        if key not in self.actions:
            return True

        return self.actions[key]()

    @property
    def pos(self):
        if self.is_live:
            return -1

        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1

    @pos.setter
    def pos(self, pos):
        if self.is_live:
            return

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)

    def _skip_time_callback(self, pos):
        self.motion.set_skip_time(pos / 1000)

    def _top_ratio_callback(self, pos):
        self.motion.set_top_ratio(pos / 1000)

    def _mid_ratio_callback(self, pos):
        self.motion.set_mid_ratio(pos / 1000)

    def _threshold_callback(self, pos):
        self.motion.set_threshold(pos)

    def _space_event(self):
        if self.roi_opened:
            self.save()
        else:
            self.paused = not self.paused

    def read(self):
        if self.paused:
            return self.frame.copy()

        _, frame = self.cap.read()
        if frame is None:
            return None

        self.frame = frame
        return frame

    def show_frame(self):
        roi_frame = self.draw_roi_frame(self.frame)

        cv2.imshow(VideoFrame.MAIN_WINDOW, roi_frame)
        binary = self.motion.binary(self.frame)
        if self.inverted:
            binary = cv2.bitwise_not(binary)
        cv2.imshow(VideoFrame.TUNING_WINDOW, binary)

        if self.roi_opened:
            cv2.imshow(VideoFrame.ROI_WINDOW, roi_frame)
        elif self.roi_opened is None:
            try:
                cv2.destroyWindow(VideoFrame.ROI_WINDOW)
            except Exception:
                ...

    def select_roi(self):
        if self.roi_opened:
            return

        self.roi_opened = True

        def _roi_wrapper(idx):
            def _roi(pos):
                self.rel_roi_box_pos[idx] = pos
                self.update_crop_box()

            return _roi

        cv2.namedWindow(VideoFrame.ROI_WINDOW)
        cv2.imshow(VideoFrame.ROI_WINDOW, self.frame)
        cv2.setMouseCallback(VideoFrame.ROI_WINDOW, self._mouse_event)
        cv2.createTrackbar("M", VideoFrame.ROI_WINDOW, self.motion.top_margin,
                           self.crop_h, self._update_margin)
        cv2.createTrackbar("W", VideoFrame.ROI_WINDOW, self.rel_roi_box_pos[2],
                           self.crop_w, _roi_wrapper(2))
        cv2.createTrackbar("H", VideoFrame.ROI_WINDOW, self.rel_roi_box_pos[3],
                           self.crop_h, _roi_wrapper(3))
        cv2.createTrackbar("X", VideoFrame.ROI_WINDOW, self.rel_roi_box_pos[0],
                           self.crop_w, _roi_wrapper(0))
        cv2.createTrackbar("Y", VideoFrame.ROI_WINDOW, self.rel_roi_box_pos[1],
                           self.crop_h, _roi_wrapper(1))

    def draw_roi_frame(self, frame):
        buff = frame.copy()

        crop_start, crop_end = _to_point_tuple_(self.crop_box_pos)
        cv2.rectangle(buff, crop_start, crop_end, (0, 0, 255), 1)

        roi_start, roi_end = _to_point_tuple_(self.roi_box_pos)
        cv2.rectangle(buff, roi_start, roi_end, (0, 255, 0), 2)

        margin = self.motion.top_margin
        x1, y1, x2, y2 = *roi_start, *roi_end
        cv2.line(buff, (x1, y1 + margin), (x2, y1 + margin), (0, 255, 0), 2)

        return buff

    def _update_margin(self, pos):
        self.motion.set_top_margin(pos)

    def _mouse_event(self, event, x, y, *_):
        if event not in {cv2.EVENT_MOUSEMOVE, cv2.EVENT_LBUTTONUP}:
            return

        self.x = x
        self.y = y
        self.update_crop_box(x, y)

        if event == cv2.EVENT_LBUTTONUP:
            self.save()

    def save(self):
        self.roi_opened = None
        self.motion.set_crop_box(*_to_point_tuple_(self.crop_box_pos))
        self.motion.set_roi_box(*_to_point_tuple_(self.roi_box_pos))
        self.save_preset()

    def update_crop_box(self, x=-1, y=-1):
        if x == -1:
            x = self.x
            y = self.y

        # update crop box
        w, h = int(self.crop_w / 2), int(self.crop_h / 2)
        self.crop_box_pos = [x - w, y - h, x + w, y + h]

    def process(self):
        frame = self.read()
        if frame is None:
            return None

        detected = self.motion.detect(frame)
        if detected is not None:
            cv2.imshow("Detected", detected)
        else:
            detected = False
        self.show_frame()
        return detected


def main(args):
    if args.debug:
        logging.basicConfig(level=logging.INFO)
        logging.info('Debug mode enabled')

    if args.save:
        makedirs(args.save, exist_ok=True)

    count = 0
    prev_time = 0

    with VideoFrame(args.frame_src, (args.width, args.height), args) as cap:
        while 1:
            detected = cap.process()
            if detected is None:
                if args.loop and not cap.is_live:
                    cap.pos = 0
                    continue
                break

            # save detected images
            if args.save and detected is not False:
                count += 1
                path = os.path.join(args.save, f'frame{count:03d}.jpg')
                cv2.imwrite(path, detected)

            # FPS control
            if cap.is_live:
                sleep_delta = 1
            else:
                now = time()
                sleep_delta = int((0.033 - (now - prev_time)) * 1000)
                if sleep_delta < 1:
                    sleep_delta = 1
                prev_time = now

            # Shortcut
            key = cv2.waitKey(sleep_delta) & 0xff
            if cap.shortcut(key) is False:
                break


def trampoline():
    parser = ArgumentParser(prog='python3 motion.py',
                            description="Motion detector tuning tool")

    parser.add_argument("-c", "--camera", type=int, help="Camera device ID")
    parser.add_argument("-l",
                        "--loop",
                        default=False,
                        action='store_true',
                        help="Loop video playback")
    parser.add_argument("-I",
                        "--invert",
                        default=False,
                        action='store_true',
                        help="Invert mask calculation")
    parser.add_argument("-F",
                        "--flip",
                        default=False,
                        action='store_true',
                        help="Flip top/mid mask calculation")
    parser.add_argument("-D",
                        "--debug",
                        default=False,
                        action='store_true',
                        help="Enable MotionDetector debug flag")
    parser.add_argument("-p",
                        "--preset",
                        default='motion.cfg',
                        type=str,
                        help="Preset file path to save")
    parser.add_argument("-P",
                        "--loadpreset",
                        type=str,
                        help="Preset file path to load")
    parser.add_argument("-k",
                        "--key",
                        default='default',
                        type=str,
                        help="Preset key to save")
    parser.add_argument("-s",
                        "--save",
                        type=str,
                        help="Set the saving path of images")
    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        nargs='?',
                        help='path of video file')
    parser.add_argument("-W",
                        "--width",
                        default=224,
                        type=int,
                        help="Crop width")
    parser.add_argument("-H",
                        "--height",
                        default=224,
                        type=int,
                        help="Crop height")

    args = parser.parse_args()

    frame_src = args.camera
    if args.path:
        frame_src = args.path
        if not exists(frame_src):
            print('[-] Invalid frame source:', frame_src)
            return

    if frame_src is None:
        parser.print_usage()
        return

    setattr(args, 'frame_src', frame_src)
    main(args)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    trampoline()
