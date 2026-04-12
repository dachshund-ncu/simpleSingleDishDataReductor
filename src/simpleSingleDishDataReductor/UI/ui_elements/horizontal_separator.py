from PyQt6 import QtWidgets

class CustomHorizontalSeparator(QtWidgets.QFrame):
    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)
        self.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.setStyleSheet("background-color: rgba(255,255,255, 25%);")
        self.setFixedHeight(1)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed)
