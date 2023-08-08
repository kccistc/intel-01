from iotdemo.color.color_label import ColorLabel
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem)

__all__ = ('ConfigTable', )


class ConfigTable(QTableWidget):

    ID_LABEL = 0
    ID_MIN = 1
    ID_MAX = 2
    ID_ITER = 3
    ID_DEL = 4

    on_select_row = pyqtSignal(ColorLabel)

    def __init__(self, parent=None):
        super(ConfigTable, self).__init__(parent)

        self.setColumnWidth(self.ID_LABEL, 270)
        self.setColumnWidth(self.ID_DEL, 1)

        self.itemSelectionChanged.connect(self.on_select)

    def index(self, name):
        for row in range(self.rowCount()):
            label_name = self.item(row, self.ID_LABEL).text()
            if label_name == name:
                return row

        return -1

    def clear(self):
        self.setRowCount(0)

    def dump(self):
        labels = []

        for row in range(self.rowCount()):
            label = self.get(row)
            labels.append((label.name, label.to_tuple()))

        return labels

    def add(self, label):
        row = self.index(label.name)
        if row == -1:
            row = self.rowCount()
            self.insertRow(row)

        # Label
        self.setItem(row, self.ID_LABEL, QTableWidgetItem(label.name))

        # Min
        item = QTableWidgetItem(', '.join(str(x) for x in label.min_range))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(row, self.ID_MIN, item)

        # Max
        item = QTableWidgetItem(', '.join(str(x) for x in label.max_range))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(row, self.ID_MAX, item)

        # Iteration
        item = QTableWidgetItem(str(label.dilate_iterations))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(row, self.ID_ITER, item)

        # Delete button
        btn = QPushButton("X")
        btn.clicked.connect(self.delete_row)
        self.setCellWidget(row, self.ID_DEL, btn)

    def get(self, row):
        name = self.item(row, self.ID_LABEL).text()
        min_value = self.item(row, self.ID_MIN).text()
        min_value = tuple(map(int, min_value.split(", ")))
        max_value = self.item(row, self.ID_MAX).text()
        max_value = tuple(map(int, max_value.split(", ")))
        dilate_iterations = int(self.item(row, self.ID_ITER).text())

        return ColorLabel(name, min_value, max_value, dilate_iterations)

    @pyqtSlot()
    def delete_row(self):
        button = self.sender()
        if button:
            row = self.indexAt(button.pos()).row()
            self.removeRow(row)

    @pyqtSlot()
    def on_select(self):
        index = self.selectionModel().selectedRows()[0]
        item = self.get(index.row())

        self.on_select_row.emit(item)
