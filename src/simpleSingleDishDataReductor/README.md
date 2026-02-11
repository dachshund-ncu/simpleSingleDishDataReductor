[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

# simpleSingleDishDataReductor
Single dish radio telescope data reductor. 
Designed to work with data, obtained from 32m NCU radio telescope autocorrelator (in both frequency-switch and on-off mode). It makes use of the QT interface and pyqtgraph plotting library to interactively visualize the data.

### Requirements ###
Bear in mind, that this package requires AT LEAST python 3.8

- PyQt5

- pyqtgraph

- mpmath

- astropy

- barycorrpy

- validators

- requests

- platformdirs


### Installation of the needed packages ###
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Usage ###
```
python3 singleDReductor.py your_archive.tar.bz2 [OPTIONS]
	OPTIONS:
	-h, --help    | show this help message and exit
	-v, --version | show version and exit
	-n, --nocal   | do not use calibration tables
	-f, --onoff   | do an on-off reduction instead of a frequency-switch
```
### Output ###
Files that go outside are in .fits format. Filename: sourcename_MJD.fits