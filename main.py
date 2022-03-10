#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# -- LIBRARY IMPORT --
import sys
sys.path.append("UI")
sys.path.append("data")
from mainWindowWidget import mainWindowWidget
from dataClass import dataContainter
from PySide2 import QtCore, QtWidgets, QtGui
# --------------------

if __name__ == "__main__":
    print("-----------------------------------------")
    print("-----> Welcome to SSDDR (Simple Single Dish Data Reductor)!")
    if (len(sys.argv) > 1):
        print("-----> Loading archive \"" + sys.argv[1] + "\"...")
    else:
        print("-----> Bad usage! You need to pass .tar.bz2 archive as a program argument!")
        print("-----------------------------------------")
        sys.exit()    
    data = dataContainter(sys.argv[1])
    app = QtWidgets.QApplication(sys.argv)
    widget = mainWindowWidget(app, data)
    widget.resize(1366, 720)
    widget.show()
    app.exec_()