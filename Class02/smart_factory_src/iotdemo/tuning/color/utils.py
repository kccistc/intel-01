from PyQt5.QtWidgets import QFileDialog

__all__ = ('save_dialog', 'load_dialog')


def save_dialog(parent):
    path = QFileDialog.getSaveFileName(parent,
                                       "Save configuration file",
                                       "color",
                                       "Config Files (*.cfg);;All Files (*)",
                                       options=QFileDialog.DontUseNativeDialog)
    if path[0] == '':
        return None

    if path[1] == 'Config Files (*.cfg)' and not path[0].endswith('.cfg'):
        return path[0] + '.cfg'

    return path[0]


def load_dialog(parent):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "Select configuration file",
        "",
        "Config Files (*.cfg);;All Files (*)",
        options=options)

    return None if not path else path
