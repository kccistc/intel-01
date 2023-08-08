#!/usr/bin/env python3

import os.path
import pathlib
import sys

import cv2
from iotdemo.color.color_detector import ColorDetector
from iotdemo.color.color_label import ColorLabel
from iotdemo.common.preset import load_preset, save_preset
from iotdemo.tuning.color.utils import load_dialog, save_dialog
from iotdemo.tuning.color.VideoThread import VideoThread
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow,
                             QTableWidgetItem)


class MainWindow(QMainWindow):
    def __init__(self, video, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(
            os.path.join(pathlib.Path(__file__).parent.resolve(), "main.ui"),
            self, 'iotdemo.tuning.color')
        self.updated = True

        if video:
            self.device = VideoThread(video, self, fps=.03)
            self.device.frame.connect(self.on_frame)
            self.device.start()
        else:
            self.device = None
            self.combo_source.addItems(
                [f"Camera {idx}" for idx in self.scan_camera_ids()])

        self.detector = ColorDetector()
        self.label = ColorLabel('', (0, 0, 0), (180, 255, 255), 0)

        self.colorslider.on_update.connect(self.colorslider_changed)
        self.table.on_select_row.connect(self.select_config)

    @staticmethod
    def scan_camera_ids(iteration=10):
        ids = []
        for idx in range(iteration):
            cap = cv2.VideoCapture(idx)
            if cap.read()[0]:
                ids.append(idx)
                cap.release()
        return ids

    def update_label(self, min_range=None, max_range=None, iteration=None):
        if min_range is not None:
            self.label.min_range = min_range
        if max_range is not None:
            self.label.max_range = max_range
        if iteration is not None:
            self.label.dilate_iterations = iteration

        self.update_ui()

    def update_ui(self):
        self.updated = False

        label = self.label
        self.line_label.setText(label.name)
        self.slider_iteration.setValue(label.dilate_iterations)

        for row, (start,
                  end) in enumerate(zip(label.min_range, label.max_range)):
            self.colorslider.set_range(row, start, end)

        self.updated = True

    # Core of main processing
    def on_frame(self, frame):
        mask = self.detector.mask(frame, self.label)
        img = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('Preview', img)

    # UI Event
    @pyqtSlot()
    def save_config_file(self):
        data = self.table.dump()
        if not data:
            return

        path = save_dialog(self)
        if not path:
            return

        save_preset(path, {name: raw for name, raw in data})

    @pyqtSlot()
    def load_config_file(self):
        path = load_dialog(self)
        if not path:
            return

        data = load_preset(path)
        for name, raw in data.items():
            label = ColorLabel(name)
            label.from_tuple(raw)
            self.table.add(label)

    @pyqtSlot()
    def add_to_config(self):
        if not self.updated:
            return

        name = self.line_label.text().strip()
        if not name:
            return

        self.label.name = name
        self.table.add(self.label)

    @pyqtSlot(tuple)
    def select_config(self, item):
        if not self.updated:
            return

        self.label = item
        self.update_ui()

    @pyqtSlot(tuple)
    def colorslider_changed(self, _):
        if not self.updated:
            return

        self.update_label(*self.colorslider.values)

    @pyqtSlot(int)
    def set_source(self, value):
        if not self.updated:
            return

        if self.device:
            self.device.stop()
            self.device = None

        self.device = VideoThread(value, self)
        self.device.frame.connect(self.on_frame)
        self.device.start()

    @pyqtSlot(int)
    def set_iteration(self, iteration):
        if not self.updated:
            return

        self.update_label(iteration=iteration)

    @pyqtSlot()
    def on_reset(self):
        if not self.updated:
            return

        self.update_label((0, 0, 0), (180, 255, 255), 0)
        self.slider_iteration.setValue(0)
        self.line_label.setText("")

    def closeEvent(self, event):
        self.on_reset()
        if self.device:
            self.device.stop()

        cv2.destroyAllWindows()
        event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

        super(MainWindow, self).keyPressEvent(e)


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    win = MainWindow(video)
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
