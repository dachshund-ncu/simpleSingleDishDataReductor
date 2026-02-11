"""
Class that holds slightly modified QWidget
"""
from PyQt5 import QtWidgets
from PyQt5 import QtCore
class custom_widget(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('''
        QWidget {
            background-color: rgba(255, 255, 255, 0%);
            border-radius: 10px;
            padding: 0px;
            font-size: 15px;
            margin-left: 0px;
            margin-right: 0px;
        }
        ''')


class CustomWidgetSemiTransparent(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('''
        QWidget {
            background-color: rgba(255, 255, 255, 5%);
            border-radius: 10px;
            padding: 0px;
            font-size: 15px;
            margin-left: 0px;
            margin-right: 0px;
            margin-top: 0px;
            margin-bottom: 0px;
        }
        ''')
#//