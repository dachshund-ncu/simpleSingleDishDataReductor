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
import numpy as np

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

    def updateDataPlots(self):
        self.scanFigure.drawData()

    def updateInfo(self):
        self.scanFigure.drawInfo()

    def setVline(self, time, ):
        self.scanFigure.tsysVline.set_data([time, time], [0,1])
        self.scanFigure.zVline.set_data([time, time], [0,1])
        self.scanFigure.totalFluxVline.set_data([time, time], [0,1])
    
    def setDots(self, time, ampTsys, zDot, totalFluxDot ):
        self.scanFigure.dot1Tsys.set_data(time[0], ampTsys[0])
        self.scanFigure.dot2Tsys.set_data(time[1], ampTsys[1])
        self.scanFigure.dot1Z.set_data(time[0], zDot[0])
        self.scanFigure.dot2Z.set_data(time[1], zDot[1])
        self.scanFigure.dotTF.set_data(time[1], totalFluxDot)

class scanStackingFigure(FigureCanvasQTAgg):
    def __init__(self):
        self.__declareNecessaryWidgets()
        super(scanStackingFigure, self).__init__(self.figure)
        plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95)
        #plt.ion()
    def __declareNecessaryWidgets(self):
        '''
        Will declare the necessary figures and axes.
        Then place them correctly inside the widget
        '''
        plt.style.use("dark_background")
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

        # other
        self.axisForZ.margins(0.2, 0.2)
        self.axisForTsys.margins(0.2, 0.2)
        self.axisForTotalFlux.margins(0.2, 0.2)

        # plottables
        self.fullYScanPlot, = self.axisForScanYFull.plot(np.nan, np.nan, c='cyan', lw=1)
        self.zoomedYScanPlot, = self.axisForScanYZoom.plot(np.nan, np.nan, c='cyan', lw=1)
        self.fitChebyPlot, = self.axisForScanYZoom.plot(np.nan, np.nan, c='magenta', lw=1)
        self.spectrumToStackPlot, = self.axisForStackedSpectrum.plot(np.nan, np.nan, c='grey', lw=1)
        self.stackPlot, = self.axisForStackedSpectrum.plot(np.nan, np.nan, c='orange', lw=1)
        self.zPlot, = self.axisForZ.plot(np.nan, np.nan, c='blue', ls="", marker='s')
        #self.tsysPlot, = self.axisForTsys.plot(np.nan, np.nan, c='blue', ls="", marker='o', mec='red', mfc="none")
        self.actualTsysPlot, = self.axisForTsys.plot(np.nan, np.nan, c='lime', ls="", marker='o', ms=6, zorder=2)
        self.totalFluxPlot, = self.axisForTotalFlux.plot(np.nan, np.nan, c='cyan', ls="", marker='o', ms=3)

        # vlines
        self.tsysVline = self.axisForTsys.axvline(np.nan, c='magenta')
        self.zVline = self.axisForZ.axvline(np.nan, c='magenta')
        self.totalFluxVline = self.axisForTotalFlux.axvline(np.nan, c='magenta')
        # dots
        self.dot1Tsys, = self.axisForTsys.plot(np.nan, np.nan, c='magenta', ls="", marker='o', ms=6, zorder=2)
        self.dot2Tsys, = self.axisForTsys.plot(np.nan, np.nan, c='magenta', ls="", marker='o', ms=6, zorder=2)
        self.dot1Z, = self.axisForZ.plot(np.nan, np.nan, c='magenta', ls="", marker='o', ms=6, zorder=2)
        self.dot2Z, = self.axisForZ.plot(np.nan, np.nan, c='magenta', ls="", marker='o', ms=6, zorder=2)
        self.dotTF, = self.axisForTotalFlux.plot(np.nan, np.nan, c='magenta', ls="", marker='o', ms=6, zorder=2)


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
    
    def drawInfo(self):
        self.__autoscaleInfo()
        self.figure.canvas.draw_idle()

    def drawData(self):
        self.__autoscaleData()
        self.figure.canvas.draw_idle()

    def __autoscaleInfo(self):
        self.axisForTsys.relim()
        self.axisForTsys.autoscale()
        self.axisForZ.relim()
        self.axisForZ.set_xlim(self.axisForTsys.get_xlim())
        self.axisForZ.autoscale(axis='y')
        self.axisForTotalFlux.relim()
        self.axisForTotalFlux.set_xlim(self.axisForTsys.get_xlim())
        self.axisForTotalFlux.autoscale(axis='y')

    def __autoscaleData(self):

        self.axisForScanYFull.relim()
        self.axisForScanYFull.autoscale(axis='x', tight=True)
        self.axisForScanYFull.autoscale(axis='y', tight=False)

        self.axisForScanYZoom.relim()
        self.axisForScanYZoom.autoscale(axis='x', tight=True)
        self.__autoscaleZoomedPlotY()

        self.axisForStackedSpectrum.relim()
        self.axisForStackedSpectrum.autoscale(axis='x', tight=True)
        self.axisForStackedSpectrum.autoscale(axis='y', tight=False)

    def __autoscaleZoomedPlotY(self):
        '''
        we need to define our own methood for autoscaling
        the zoomedYScanPlot, because we want it zoomed ;)
        '''
        y = self.fitChebyPlot.get_ydata()
        max = y.max()
        min = y.min()
        diff = max-min
        lowerEnd = min - 2.0 * diff
        upperEnd = max + 2.0 * diff
        self.axisForScanYZoom.set_ylim(lowerEnd, upperEnd)

