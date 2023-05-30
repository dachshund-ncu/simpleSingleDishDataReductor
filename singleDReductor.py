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
# -- IMPORT BLOCK --
import sys
from PyQt5 import QtWidgets, QtGui
import os

# managing source dirname to properly import custom classes:
scr_directory = os.path.dirname(__file__) + '/'
sys.path.append(scr_directory)
sys.path.append(scr_directory + "UI")
sys.path.append(scr_directory + "data")
from mainWindowWidget import mainWindowWidget
from dataClass import dataContainter
# --------------------

def ohHelp():
    print("-----> Usage:")
    print("\tpython3 singleDReductor.py your_archive.tar.bz2 [OPTIONS]")
    print("\tOPTIONS:")
    print("\t-h, --help    | show this help message and exit")
    print("\t-v, --version | show version and exit")
    print("\t-n, --nocal   | do not use calibration tables")
    print("\t-f, --onoff   | do an on-off reduction instead of a frequency-switch")
    print("-----------------------------------------")
    sys.exit()

def onVersion():
    print("-----> This is \"Simple Single Dish Data Reductior\"")
    print("-----> Author: Michał Durjasz, Nicolaus Copernicus Univesity, Poland")
    print("-----> E-mail: md@astro.umk.pl")
    print("-----> Version: 1.1")
    print("-----------------------------------------")
    sys.exit()


if __name__ == "__main__":
    """
    This is main of the SSDDR
    - we print here welcome message and wake to life objects, used in the process of data reduction
    - we also need to program invocation around -nocal option    
    """

    print("-----------------------------------------")
    print("-----> Welcome to SSDDR (Simple Single Dish Data Reductor)!")
    print("-----------------------------------------")
    if (len(sys.argv) > 1):
        pass
    else:
        print("-----> Bad usage! You need to pass .tar.bz2 archive as a program argument!")
        print("-----------------------------------------")
        sys.exit()    
    app = QtWidgets.QApplication(sys.argv)

    if '-v' in sys.argv or '--version' in sys.argv:
        onVersion()
    elif '-h' in sys.argv or '--help' in sys.argv:
        ohHelp()

    if '-f' in sys.argv or '--onoff' in sys.argv:
        onOff = True
    else:
        onOff = False

    if '--nocal' in sys.argv or '-n' in sys.argv:
        '''
        We need to program this app for two cases:
        ./singleDreductor.py archive.tar.bz2 --nocal
        and
        ./singleDreductor.py --nocal archive.tar.bz2
        '''
        if '--nocal' in sys.argv:
            nocalIndex = sys.argv.index('--nocal')
        elif '-n' in sys.argv:
            nocalIndex = sys.argv.index('-n')

        if nocalIndex == 1:
            data = dataContainter(scr_directory, sys.argv[2], onOff)
        else:
            data = dataContainter(scr_directory, sys.argv[1], onOff)
        widget = mainWindowWidget(app, data, calibrate=False)
    else:
        data = dataContainter(scr_directory, sys.argv[1], onOff)
        widget = mainWindowWidget(app, data, calibrate=True)
    
    widget.setWindowIcon(QtGui.QIcon(scr_directory + "icons/satellite-dish.png"))
    widget.setWindowTitle("Data reduction: " + data.obs.scans[0].sourcename + " " + data.obs.scans[0].isotime)
    widget.resize(1366, 720)
    widget.show()
    app.exec_()