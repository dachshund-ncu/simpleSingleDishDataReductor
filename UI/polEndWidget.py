'''
This class holds widget for polarization reduction end
'''


from PySide2 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
import numpy as np


class polEndWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        Initializing the widget
        -> declare figures etc.
        '''
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.polEndFIg = polEndFigure()
        self.layout.addWidget(self.polEndFIg)
    
    def plotSpectrum(self, x, y):
        self.polEndFIg.plotSpectrum(x,y)

class polEndFigure(FigureCanvasQTAgg):
    def __init__(self):
        self.__declareNecessaryWidgets()
        super(polEndFigure, self).__init__(self.figure)
        plt.subplots_adjust(top=0.98, bottom=0.08, left=0.08, right=0.98)
    
    def __declareNecessaryWidgets(self):
        plt.style.use("dark_background")
        self.figure = plt.figure()

        self.gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
        self.specAxis = self.figure.add_subplot(self.gs[0,0])
        self.caltabPlot = self.figure.add_subplot(self.gs[1,0])

        self.__makeFancyTicks(self.specAxis)
        self.__makeFancyTicks(self.caltabPlot)

        self.spectrumPlot, = self.specAxis.plot(np.nan, np.nan, c='cyan', lw=1)

        self.specAxis.set_ylabel("Amplitude")
        self.specAxis.set_xlabel(r"V$_{\mathrm{lsr}}\,$(km$\,$s$^{-1}$)")
        self.caltabPlot.set_xlabel("MJD")
        self.caltabPlot.set_ylabel("Cal coeff.")
    def __makeFancyTicks(self, ax):
        ax.xaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    def plotSpectrum(self, x,y):
        self.spectrumPlot.set_data(x,y)
        self.specAxis.relim()
        self.specAxis.autoscale(axis='x', tight=True)
        self.specAxis.autoscale(axis='y', tight=False)
        self.figure.canvas.draw_idle()