[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

# simpleSingleDishDataReductor
Single dish radio telescope data reductor. 
Designed to work with data, obtained from 32m NCU radio telescope autocorrelator (in frequency-switch mode). It makes use of the QT interface and pyqtgraph plotting library to interactively visualize the data.

### Requirements ###

- PySide2

- pyqtgraph

- mpmath

- astropy

- barycorrpy

- validators

- requests

### Installation of the needed packages ###
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Usage ###
```bash
python3 singleDReductor.py your_archive_name.tar.bz2
```
### Output ###
Files that go outside are in .fits format. Filename: sourcename_MJD.fits