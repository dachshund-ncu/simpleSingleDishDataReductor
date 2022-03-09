#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# -- LIBRARY IMPORT --
import sys
sys.path.append("UI")
sys.path.append("data")
from mainWindowWidget import mainWindowWidget
from PySide2 import QtCore, QtWidgets, QtGui
# --------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = mainWindowWidget(app)
    widget.resize(1366, 720)
    widget.show()
    app.exec_()