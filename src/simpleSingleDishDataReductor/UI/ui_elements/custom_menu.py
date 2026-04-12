"""
Class that holds slightly modified QWidget
"""
from PyQt6 import QtWidgets


class CustomMenu(QtWidgets.QMenu):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)


