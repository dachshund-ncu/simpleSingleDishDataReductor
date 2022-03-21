'''
Class that holds custom buyyon
Just to avoid repeating code
'''

from PySide2 import QtWidgets
'''
QPushButton#evilButton {
    background-color: red;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px;
}
'''
class cButton(QtWidgets.QPushButton):
    def __init__(self, name = ''):
        super().__init__()

        self.setMaximumSize(10000, 10000)
        self.setMinimumSize(0, 0)
        self.setText(name)
    def setColor(self, colorname):
        self.setStyleSheet(f"background-color: {colorname}")