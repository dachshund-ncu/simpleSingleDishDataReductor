"""
Class that holds slightly modified QWidget
"""
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class cWidget(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('''
        QWidget{
             background-color: rgba(255, 255, 255, 0%);
             border-radius: 10px;
             padding: 0px;
             margin-left: 0px;
        }
         ''')
        self.setMinimumSize(220, 720)
        self.setMaximumSize(220, 99999)
