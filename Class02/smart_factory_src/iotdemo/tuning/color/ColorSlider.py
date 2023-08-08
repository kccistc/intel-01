from functools import partial

from iotdemo.tuning.color.QRangeSlider import QRangeSlider
from PyQt5.QtCore import QCoreApplication, QMetaObject, pyqtSignal
from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget

__all__ = ('ColorSlider', )


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("ColorSlider")

        layout = QFormLayout(Form)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        layout.setObjectName("layout")
        self.layout = layout

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("ColorSlider", "ColorSlider"))


class ColorSlider(QWidget, Ui_Form):

    on_update = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(ColorSlider, self).__init__(parent)
        self.setupUi(self)

        self.min_prev = (-1, -1)
        self.max_prev = (-1, -1)

        for idx, (label, min_value, max_value, color) in enumerate(
            (('H', 0, 180, '#999'), ('S', 0, 255, '#c90000'), ('V', 0, 255,
                                                               '#0031a3'))):
            slider = QRangeSlider(self)
            slider.setMin(min_value)
            slider.setMax(max_value)
            slider.setRange(min_value, max_value)
            slider.handle.setStyleSheet(f'background: {color};')

            slider.startValueChanged.connect(partial(self.update_min, idx))
            slider.endValueChanged.connect(partial(self.update_max, idx))

            self.layout.addRow(QLabel(label), slider)

    def set_range(self, ch, start, end):
        self.layout.itemAt(ch, 1).widget().setRange(start, end)

    def update_min(self, ch, value):
        _ch, _value = self.min_prev
        if _ch == ch and _value == value:
            return

        self.min_prev = (ch, value)
        self.on_update.emit(('min', ch, value))

    def update_max(self, ch, value):
        _ch, _value = self.max_prev
        if _ch == ch and _value == value:
            return

        self.max_prev = (ch, value)
        self.on_update.emit(('max', ch, value))

    @property
    def values(self):
        min_value = []
        max_value = []

        for row in range(3):
            slider = self.layout.itemAt(row, 1).widget()
            min_value.append(slider.start())
            max_value.append(slider.end())

        return tuple(min_value), tuple(max_value)
