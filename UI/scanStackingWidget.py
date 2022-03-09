'''
Class, that holds the scan stacking widget:
-> plotting actual scans
-> plotting stacked spectrum 
-> plotting z(t), tsys(t), total flux(t)
-> labels: scans, tsys, rms, snr, peak
'''

from PySide2 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator

class scanStackingWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        initializing the widget:
        -> will initialize the layout
        -> will declare necessary widgets and place them correctly
        '''
        super().__init__()
        self.layout = QtWidgets.QGridLayout(self)
        self.scanFigure = scanStackingFigure()
        self.layout.addWidget(self.scanFigure)

class scanStackingFigure(FigureCanvasQTAgg):
    def __init__(self):
        self.__declareNecessaryWidgets()
        super(scanStackingFigure, self).__init__(self.figure)
        plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95)
    def __declareNecessaryWidgets(self):
        '''
        Will declare the necessary figures and axes.
        Then place them correctly inside the widget
        '''
        self.figure = plt.figure()

        # outer GS
        self.gs = gridspec.GridSpec(3,2, width_ratios=[2,1], figure=self.figure, wspace=0.1)
        self.axisForScan = self.figure.add_subplot(self.gs[0:2,0])
        self.axisForStackedSpectrum = self.figure.add_subplot(self.gs[2,0])
        self.axisForOthers = self.figure.add_subplot(self.gs[0:2, 1])

        # inner GS
        self.axisForScanGS = gridspec.GridSpecFromSubplotSpec(2,1, hspace=0.0, subplot_spec=self.axisForScan)
        self.axisForScanYFull = self.figure.add_subplot(self.axisForScanGS[0,0])
        self.axisForScanYZoom = self.figure.add_subplot(self.axisForScanGS[1,0])

        self.axisForOthersGS = gridspec.GridSpecFromSubplotSpec(3,1, hspace=0.0, subplot_spec=self.axisForOthers)
        self.axisForZ = self.figure.add_subplot(self.axisForOthersGS[0,0])
        self.axisForTsys = self.figure.add_subplot(self.axisForOthersGS[1,0])
        self.axisForTotalFlux = self.figure.add_subplot(self.axisForOthersGS[2,0])

        # other plottable-specific settings
        self.axisForZ.yaxis.tick_right()
        self.axisForZ.yaxis.set_label_position("right")
        self.axisForTsys.yaxis.tick_right()
        self.axisForTsys.yaxis.set_label_position("right")
        self.axisForTotalFlux.yaxis.tick_right()
        self.axisForTotalFlux.yaxis.set_label_position("right")

        self.axisForScanYFull.set_xticklabels([])
        self.axisForZ.set_xticklabels([])
        self.axisForTsys.set_xticklabels([])

        # fancy handling
        self.__clearPlottable(self.axisForScan)
        self.__clearPlottable(self.axisForOthers)
        self.__makeFancyTicks(self.axisForStackedSpectrum)
        self.__makeFancyTicks(self.axisForScanYFull)
        self.__makeFancyTicks(self.axisForScanYZoom)
        self.__makeFancyTicks(self.axisForZ)
        self.__makeFancyTicks(self.axisForTsys)
        self.__makeFancyTicks(self.axisForTotalFlux)

        # labels
        self.axisForZ.set_ylabel("Z$\,$($^{\circ}$)")
        self.axisForTsys.set_ylabel("T$_{\mathrm{sys}}\,$(K)")
        self.axisForTotalFlux.set_ylabel("Total flux")

    def __clearPlottable(self, ax):
        ax.set_yticks([])
        ax.set_xticks([])

    def __makeFancyTicks(self, ax):
        ax.xaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())