#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This is MAIN fo simpleSingleDishDataRecuctot
Author: Michał Durjasz
E-mail: md@astro.umk.pl

attributions:
Radar icon used in this app is created by Freepik:
https://www.flaticon.com/free-icons/radar
'''
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

palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.WindowText, QtGui.Qt.white)
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.Qt.black)
palette.setColor(QtGui.QPalette.ToolTipText, QtGui.Qt.white)
palette.setColor(QtGui.QPalette.Text, QtGui.Qt.white)
palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
palette.setColor(QtGui.QPalette.ButtonText, QtGui.Qt.white)
palette.setColor(QtGui.QPalette.BrightText, QtGui.Qt.red)
palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
palette.setColor(QtGui.QPalette.HighlightedText, QtGui.Qt.black)

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
    app.setStyle("Fusion")
    app.setPalette(palette)
    if '-nocal' in sys.argv:
        widget = mainWindowWidget(app, data, calibrate=False)
    else:
        widget = mainWindowWidget(app, data, calibrate=True)
    widget.setWindowIcon(QtGui.QIcon(scr_directory + "icons/satellite-dish.png"))
    widget.setWindowTitle("Data reduction: " + data.obs.scans[0].sourcename + " " + data.obs.scans[0].isotime)
    widget.resize(1366, 720)
    widget.show()
    app.exec_()