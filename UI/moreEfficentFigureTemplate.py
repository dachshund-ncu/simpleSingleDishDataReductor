'''
More efficcient figure template in pyQtGraph
'''
import pyqtgraph as pg
from PySide2 import QtGui, QtWidgets, QtCore
import numpy as np

class templateFigurePG(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        #x = np.linspace(-10, 10)
        #y = np.sin(x) / x
        #self.plot(x, y)
        self.setVisible(True)
