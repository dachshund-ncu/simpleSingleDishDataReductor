#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is MAIN fo simpleSingleDishDataRecuctot
Author: Michał Durjasz
E-mail: md@astro.umk.pl

attributions:
Radar icon used in this app is created by Freepik:
https://www.flaticon.com/free-icons/radar
"""
# -- IMPORT BLOCK --
import sys
from PyQt6 import QtWidgets, QtGui
import os
from .UI.mainWindowWidget import mainWindowWidget
import argparse
import json
# --------------------

DE_CAT: str = os.path.dirname(__file__)
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
    parser = argparse.ArgumentParser(description=f"Data reduction tool for 32-m NCU RT spectral data. Version {CONFIG['version']}.")
    parser.add_argument("-n", "--nocal", action="store_true", help="do not use calibration tables")
    parser.add_argument("-f", "--onoff", action="store_true", help="do an on-off reduction instead of a frequency-switch")
    parser.add_argument("filename", nargs='?', default=None, help=".tar.bz2 archive filename")
    args = parser.parse_args()

    # -- construct greeting --
    construct_greeting(args)

    # -- start app --
    app = QtWidgets.QApplication(sys.argv)
    widget = mainWindowWidget(
        software_path = DE_CAT,
        target_filename = args.filename,
        is_on_off=args.onoff,
        calibrate = not args.nocal)

    # -- go --
    app.exec()

if __name__ == "__main__":
    main()