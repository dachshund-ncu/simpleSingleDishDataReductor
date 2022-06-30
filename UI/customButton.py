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
    def __init__(self, text, parent = None):
        super().__init__(text, parent)
        self.setMinimumSize(0,0)
        self.setMaximumSize(9999, 9999)
        self.__setMyStyle()
    def __setMyStyle(self):
        self.setStyleSheet \
        (
            "QPushButton \
            { \
                color: black; \
                background-color: #D3D3D3; \
                selection-background-color: darkgrey; \
                border-style: outset; \
                border-width: 0px; \
                border-radius: 8px; \
                border-color: transparent\
            }"
            "QPushButton:hover \
            { \
                background-color: silver\
            }"
            "QPushButton:pressed \
            { \
                background-color: white\
            }"
            "QPushButton:disabled \
             { \
                background-color: #696969\
             }"
            "QPushButton:checked \
             { \
                background-color: #778899\
             }"
            
        )
    
    def setColorX(self, color):
        self.setStyleSheet \
        (
            "QPushButton \
            { \
                color: black; \
                background-color: %s; \
                selection-background-color: darkgrey; \
                border-style: outset; \
                border-width: 0px; \
                border-radius: 0px; \
            }"
            "QPushButton:hover \
            { \
                background-color: darkgrey\
            }"
            "QPushButton:pressed \
            { \
                background-color: white\
            }" % (color)            
        )