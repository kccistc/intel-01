"""
Simple color detection algorithm
"""
from logging import getLogger
from time import time

import cv2
import numpy as np
from iotdemo.color.color_label import ColorLabel
from iotdemo.common.preset import load_preset, save_preset

__all__ = ('ColorDetector', )


class ColorDetector:
    """
    Simple color detect class
    """
    def __init__(self, *, debug=False):
        self.debug = debug
        if self.debug:
            self.logger = getLogger('COLOR')

        self.labels = []

    @property
    def preset(self):
        return {label.name: label.to_tuple() for label in self.labels}

    def load_preset(self,
                    path: str = 'color.cfg',
                    key: str = 'default',
                    *,
                    default: bool = False):
        if self.debug:
            self.logger.info('load preset from %s / %s', path, key)

        data = load_preset(path, key)
        if data is None:
            return

        labels = []
        for name, value in data.items():
            label = ColorLabel(name)
            label.from_tuple(value)
            labels.append(label)

        self.labels = labels

    def save_preset(self, path: str, key: str = 'default'):
        save_preset(path, self.preset, key)

    def mask(self, frame, label, *, is_hsv=False):
        hsv = frame if is_hsv else cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, label.min_range, label.max_range)
        if label.dilate_iterations:
            mask = cv2.dilate(mask, None, iterations=label.dilate_iterations)

        return mask

    def detect(self, frame):
        h, w, *_ = frame.shape
        total_pixels = w * h

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        result = []
        for label in self.labels:
            mask = self.mask(hsv, label, is_hsv=True)
            if self.debug:
                cv2.imshow(f'Debug: {label.name}', mask)

            result.append((label.name, cv2.countNonZero(mask) / total_pixels))

        return sorted(result, key=lambda o: o[1], reverse=True)
