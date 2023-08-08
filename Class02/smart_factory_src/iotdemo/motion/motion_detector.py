"""
Simple motion detection algorithm
"""
from logging import getLogger
from time import time

import cv2
import numpy as np
from iotdemo.common.preset import load_preset, save_preset

__all__ = ('MotionDetector', )


class MotionDetector:
    """
    Simple motion detect class to extract best shot
    """
    EMPTY_POINT = (0, 0)
    EMPTY_BOX = (EMPTY_POINT, EMPTY_POINT)
    EMPTY_AREA = np.s_[0:0, 0:0]

    DEFAULT_INVERTED = False
    DEFAULT_FLIPPED = False
    DEFAULT_TOP_MARGIN = 10
    DEFAULT_THRESHOLD = 127
    DEFAULT_TOP_RATIO = .6
    DEFAULT_MID_RATIO = .4
    DEFAULT_SKIP_TIME = .099  # less then 99ms (3 frame - 30 fps)

    def __init__(self, *, debug=False):
        self.debug = debug
        if self.debug:
            self.logger = getLogger('MOTION')

        self.inverted = MotionDetector.DEFAULT_INVERTED
        self.flipped = MotionDetector.DEFAULT_FLIPPED

        self.top_margin = MotionDetector.DEFAULT_TOP_MARGIN
        self.threshold = MotionDetector.DEFAULT_THRESHOLD

        self.top_ratio = MotionDetector.DEFAULT_TOP_RATIO
        self.mid_ratio = MotionDetector.DEFAULT_MID_RATIO

        self.skip_time = MotionDetector.DEFAULT_SKIP_TIME

        self.roi_box = MotionDetector.EMPTY_BOX
        self.roi_area = MotionDetector.EMPTY_AREA

        # optional
        self.crop_box = MotionDetector.EMPTY_BOX
        self.crop_area = MotionDetector.EMPTY_AREA

        self.total_top_pixels = 0
        self.total_mid_pixels = 0

        self.prev_time = 0

        self.changed = False

    @property
    def preset(self):
        return {
            'inverted': self.inverted,
            'flipped': self.flipped,
            'top_margin': self.top_margin,
            'threshold': self.threshold,
            'top_ratio': self.top_ratio,
            'mid_ratio': self.mid_ratio,
            'skip_time': self.skip_time,
            'roi_top_left': self.roi_box[0],
            'roi_bottom_right': self.roi_box[1],
            'crop_top_left': self.crop_box[0],
            'crop_bottom_right': self.crop_box[1],
        }

    def load_preset(self,
                    path: str = 'motion.cfg',
                    key: str = 'default',
                    *,
                    default: bool = False):
        if self.debug:
            self.logger.info('load preset from %s / %s', path, key)

        if default:
            data = {}
        else:
            data = load_preset(path, key)
            if data is None:
                return

        self.flipped = data.get('flipped', MotionDetector.DEFAULT_FLIPPED)
        self.inverted = data.get('inverted', MotionDetector.DEFAULT_INVERTED)

        self.top_margin = data.get('top_margin',
                                   MotionDetector.DEFAULT_TOP_MARGIN)
        self.threshold = data.get('threshold',
                                  MotionDetector.DEFAULT_THRESHOLD)

        self.top_ratio = data.get('top_ratio',
                                  MotionDetector.DEFAULT_TOP_RATIO)
        self.mid_ratio = data.get('mid_ratio',
                                  MotionDetector.DEFAULT_MID_RATIO)

        self.skip_time = data.get('skip_time',
                                  MotionDetector.DEFAULT_SKIP_TIME)

        roi_top_left = data.get('roi_top_left', (12, 0))
        roi_bottom_right = data.get('roi_bottom_right', (212, 90))
        self.set_roi_box(roi_top_left, roi_bottom_right)

        crop_top_left = data.get('crop_top_left', (0, 10))
        crop_bottom_right = data.get('crop_bottom_right', (224, 234))
        self.set_crop_box(crop_top_left, crop_bottom_right)
        self.changed = False

    def save_preset(self, path: str, key: str = 'default'):
        save_preset(path, self.preset, key)
        self.changed = False

    @property
    def crop_size(self):
        (x1, y1), (x2, y2) = self.crop_box
        return (x2 - x1), (y2 - y1)

    def set_inverted(self, inverted: bool):
        if self.inverted == inverted:
            return

        self.inverted = inverted
        self.changed = True

    def set_flipped(self, flipped: bool):
        if self.flipped == flipped:
            return

        self.flipped = flipped
        self.changed = True

    def set_threshold(self, threshold: int):
        if self.threshold == threshold:
            return

        self.threshold = threshold
        self.changed = True

    def set_top_ratio(self, ratio: float):
        if self.top_ratio == ratio:
            return

        self.top_ratio = ratio
        self.changed = True

    def set_mid_ratio(self, ratio: float):
        if self.mid_ratio == ratio:
            return

        self.mid_ratio = ratio
        self.changed = True

    def set_skip_time(self, skip_time: float):
        if self.skip_time == skip_time:
            return

        self.skip_time = skip_time
        self.prev_time = 0
        self.changed = True

    def set_roi_box(self, top_left: tuple, bottom_right: tuple):
        (x1, y1), (x2, y2) = self.roi_box = (top_left, bottom_right)
        self.roi_area = np.s_[y1:y2, x1:x2]

        self.set_top_margin()
        self.changed = True

    def set_crop_box(self, top_left: tuple, bottom_right: tuple):
        (x1, y1), (x2, y2) = self.crop_box = (top_left, bottom_right)
        self.crop_area = np.s_[y1:y2, x1:x2]
        self.changed = True

    def reset_crop_box(self):
        self.crop_box = MotionDetector.EMPTY_BOX
        self.crop_area = MotionDetector.EMPTY_AREA
        self.changed = True

    def set_top_margin(self, top_margin: int = -1):
        if top_margin != -1:
            self.top_margin = top_margin

        (x1, y1), (x2, y2) = self.roi_box
        w = x2 - x1
        h = y2 - y1

        self.total_top_pixels = w * self.top_margin
        self.total_mid_pixels = w * (h - self.top_margin)
        self.changed = True

    def measure(self, binary):
        # Top Area
        target_pixels = cv2.countNonZero(binary[:self.top_margin, :])
        if self.inverted:
            target_pixels = self.total_top_pixels - target_pixels

        delta_top = target_pixels / self.total_top_pixels
        if self.debug:
            self.logger.info('TOP AREA ratio: %f %s (%f)', delta_top,
                             '>' if self.flipped else '<', self.top_ratio)

        if self.flipped:
            if delta_top < self.top_ratio:
                return False
        else:
            if delta_top > self.top_ratio:
                return False

        # Mid Area
        target_pixels = cv2.countNonZero(binary[self.top_margin:, :])
        if self.inverted:
            target_pixels = self.total_mid_pixels - target_pixels

        delta_mid = target_pixels / self.total_mid_pixels
        if self.debug:
            self.logger.info('mid area ratio: %f %s (%f)', delta_mid,
                             '<' if self.flipped else '>', self.mid_ratio)

        if self.flipped:
            if delta_mid > self.mid_ratio:
                return False
        else:
            if delta_mid < self.mid_ratio:
                return False

        return True

    def binary(self, frame):
        # merge channels and apply threshold
        value = np.maximum.reduce(cv2.split(frame))
        return cv2.threshold(value, self.threshold, 255, cv2.THRESH_BINARY)[1]

    def detect(self, frame):
        if self.total_top_pixels == 0 or self.total_mid_pixels == 0:
            return None

        roi_frame = frame if self.roi_area == MotionDetector.EMPTY_AREA else frame[
            self.roi_area]
        value = self.binary(roi_frame)

        if self.debug:
            cv2.imshow('ROI frame', roi_frame)
            if self.inverted:
                cv2.imshow('ROI frame - threshold (inverted)',
                           cv2.bitwise_not(value))
            else:
                cv2.imshow('ROI frame - threshold', value)

        if not self.measure(value):
            return None

        # debounce time
        now = time()
        delta = now - self.prev_time
        self.prev_time = now
        if delta < self.skip_time:
            return None

        if self.crop_area != MotionDetector.EMPTY_AREA:
            return frame[self.crop_area]
        else:
            return frame
