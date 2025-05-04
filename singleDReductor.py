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
from UI.mainWindowWidget import mainWindowWidget
from data.dataClass import dataContainter
import argparse
import json
from UI.icons import satellite_dish
# --------------------

DE_CAT = os.path.dirname(__file__)
CONFIG = json.load(
    open(
        os.path.join(DE_CAT, "config.json"),
        "r+"))


def construct_greeting(args: argparse.Namespace):
    print("-----> Welcome to the SSDDR!")
    if args.nocal:
        print("-----> --nocal option used. Calibration tables will not be applied")
    if args.onoff:
        print("-----> --onoff option used. The data will be processed in on-off method")


def main():
    """
    This is main of the SSDDR
    """
    # -- parse arguments --
    parser = argparse.ArgumentParser(description=f"Data reduction tool for 32-m NCU RT spectral data. Version {CONFIG["version"]}.")
    parser.add_argument("-n", "--nocal", action="store_true", help="do not use calibration tables")
    parser.add_argument("-f", "--onoff", action="store_true", help="do an on-off reduction instead of a frequency-switch")
    parser.add_argument("filename")
    args = parser.parse_args()

    # -- construct greeting --
    construct_greeting(args)

    # -- start app --
    app = QtWidgets.QApplication(sys.argv)
    data = dataContainter(
        software_path = DE_CAT,
        target_filename = args.filename,
        onOff=args.onoff)
    widget = mainWindowWidget(
        data,
        calibrate = not args.nocal)

    # -- set window properties
    widget.setWindowIcon(satellite_dish)
    widget.setWindowTitle("Data reduction: " + data.obs.scans[0].sourcename + " " + data.obs.scans[0].isotime)
    widget.resize(1366, 720)
    widget.show()

    # -- go --
    app.exec_()

if __name__ == "__main__":
    main()