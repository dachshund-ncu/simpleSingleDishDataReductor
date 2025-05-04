'''
Class that holds custom buyyon
Just to avoid repeating code
'''

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

class custom_button(QtWidgets.QPushButton):
    def __init__(self, *args):
        QtWidgets.QPushButton.__init__(self, *args)
        self.setMaximumSize(9999, 70)
        self.setIconSize(QtCore.QSize(20,20))
        self.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: transparent;
                border: none;
                padding: 6px 10px;
                text-align: left;
                font-size: 14px;
                border-radius: 8px;
                font-family: silka;
                margin-top: 0px;
                margin-bottom: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,12%);
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,15%);
            }
            QPushButton:checked {
                background-color: #C2185B;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:disabled {
                color: grey;
            }
        ''')

        # self.__add_icon_to_button(os.path.join(os.path.dirname(os.path.dirname(__file__)), "ASSETS", "load_icon.svg"))

    def __add_icon_to_button(self, icon_name: str):
        icon = QtGui.QIcon(icon_name)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(20, 20))
    
    def setColorX(self, color):
        self.setStyleSheet \
            (
               "QPushButton {\
                   background-color: %s; \
                   color: white;\
                   padding: 12px; \
                   font-size: 14px; \
                   border-radius: 6px; \
                   text-align:left;\
                   font-family: silka;\
               }\
               QPushButton:hover {\
                   background-color: #FFFFFF12; \
                   border: 1px solid #FFFFFF26;\
               }\
               QPushButton:pressed {\
                   background-color: #FFFFFF1E; \
                   border: 1px solid #FFFFFF26;\
               }" % color
            )