"""
Class that holds slightly modified QWidget
"""
from PyQt5 import QtWidgets
from PyQt5 import QtCore
class CustomMenu(QtWidgets.QMenu):
    def __init__(self, *args):
        QtWidgets.QMenu.__init__(self, *args)
        self.styleSheet = R'''
            QMenuBar {
                background-color: transparent;
            }
            QMenuBar::item{
                background-color: transparent;
                padding: 8px; /* padding */
                border-radius: 2px; /* border radius */
                font-size: 12px; /* font size */
                text-align: left;
                font-family: silka;
                color: white; /* text color */
            }
            QMenuBar::item:selected {
                background-color: rgba(255,255,255,9%);
            }
            QMenu {
                background-color: #121212;
                color: white; /* text color */
                padding: 4px; /* padding */
                font-size: 12px; /* font size */
                border-radius: 2px; /* border radius */
                text-align: left;
                font-family: silka;
            }
            QAction{
                color: white; /* text color */
                padding: 4px; /* padding */
                font-size: 15px; /* font size */
                border-radius: 2px; /* border radius */
                text-align: left;
                font-family: silka;
            }
            QMenu::item {
                background-color: #121212;
                padding: 8px 12px;
                border-radius: 2px; /* border radius */
            }
            QMenu::item:selected {
                background-color: rgba(255,255,255,9%);
                border: 1px solid rgba(255,255,255,50%);
            }
            QMenu::item:checked {
                background-color: #C2185B;
            }
        '''
        self.setStyleSheet(self.styleSheet)