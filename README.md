[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

# simpleSingleDishDataReductor
Single dish radio telescope data reductor. 
Designed to work with data, obtained from 32m NCU radio telescope autocorrelator (in both frequency-switch and on-off mode). It makes use of the QT interface and pyqtgraph plotting library to interactively visualize the data.

### Requirements
This package requires AT LEAST python 3.10

### Installation
Can be installed via pip

```bash
# in repository main directory
python3 -m pip install .
```
or via [UV](https://docs.astral.sh/uv)
```bash
# in repository main directory
uv sync
uv tool install .
```
### Running
When installed via pip
```bash
# anywhere
python3 -m pip simpleSingleDishDataReductor
```

when installed bia UV
```bash
# anywhere
sdred
```


### Help
```
usage: sdred [-h] [-n] [-f] [filename]

Data reduction tool for 32-m NCU RT spectral data. Version 1.14.

positional arguments:
  filename     .tar.bz2 archive filename

options:
  -h, --help   show this help message and exit
  -n, --nocal  do not use calibration tables
  -f, --onoff  do an on-off reduction instead of a frequency-switch
```

### Output ###
Files that go outside are in .fits format. Filename: sourcename_MJD.fits
