'''
Class that holds slightly modified QWidget
'''
from PySide2 import QtWidgets

class cWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setMinimumSize(220, 720)
        self.setMaximumSize(220, 99999)