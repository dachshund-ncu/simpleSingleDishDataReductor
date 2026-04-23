"""
Class that holds slightly modified QWidget
"""
from PyQt6 import QtWidgets
from PyQt6 import QtCore
class custom_widget(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('''
        QWidget {
            background-color: rgba(255, 255, 255, 0%);
            border-radius: 10px;
            padding: 0px;
            font-size: 15px;
            margin: 1px;
        }
        ''')


class CustomWidgetSemiTransparent(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('''
            CustomWidgetSemiTransparent {
                background-color: rgba(255, 255, 255, 5%);
                border: 0.5px solid rgba(255, 255, 255, 15%);
                border-radius: 10px;
                padding: 0px;
                font-size: 15px;
                margin-left: 1px;
                margin-right: 1px;
                margin-top: 1px;
                margin-bottom: 1px;
            }
            ''')

