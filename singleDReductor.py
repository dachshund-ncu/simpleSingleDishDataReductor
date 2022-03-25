#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# -- LIBRARY IMPORT --
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from os.path import realpath

# -- custom widgets etc. --
scr_directory = realpath(__file__)
tmp = scr_directory.split('/')
scr_directory = ""
for i in range(len(tmp)-1):
    scr_directory += tmp[i] + '/'
sys.path.append(scr_directory)
sys.path.append(scr_directory + "UI")
sys.path.append(scr_directory + "data")
from mainWindowWidget import mainWindowWidget
from dataClass import dataContainter

# --------------------

if __name__ == "__main__":
    print("-----------------------------------------")
    print("-----> Welcome to SSDDR (Simple Single Dish Data Reductor)!")
    print("-----------------------------------------")
    if (len(sys.argv) > 1):
        pass
    else:
        print("-----> Bad usage! You need to pass .tar.bz2 archive as a program argument!")
        print("-----------------------------------------")
        sys.exit()    
    data = dataContainter(scr_directory, sys.argv[1])
    app = QtWidgets.QApplication(sys.argv)
    if '-nocal' in sys.argv:
        widget = mainWindowWidget(app, data, calibrate=False)
    else:
        widget = mainWindowWidget(app, data, calibrate=True)
    widget.resize(1366, 720)
    widget.show()
    app.exec_()