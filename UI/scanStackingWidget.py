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
        self.__declareNecessaryButtons()
        self.__placeNecessaryButtons()
        self.__defaultSettings()

        # -------------------------
        self.clickedOnce = False
        self.fitDone = True
        self.fitBoundsChannels = [
            [10, 824],
            [1224, 2872],
            [3272, 4086]
        ]
        self.tmpChans = []
        # -------------------------

        self.removeDone = True
        self.removeChannelsTab = []
        self.polyFitMode = True
        self.removeChannelsMode = False
        self.autoRedMode = False
        
        id = self.scanFigure.figure.canvas.mpl_connect('button_press_event', self.__onClick)

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
    
    def __declareNecessaryButtons(self):
        self.vboxMainOperationsFrame = QtWidgets.QVBoxLayout()
        self.mainOperationsFrame = QtWidgets.QGroupBox("Main operations")
        self.mainOperationsFrame.setLayout(self.vboxMainOperationsFrame)
        self.vboxChannelHandling = QtWidgets.QVBoxLayout()
        self.channelHandlingFrame = QtWidgets.QGroupBox("Channel handling")
        self.channelHandlingFrame.setLayout(self.vboxChannelHandling)
        self.nextPrevScanLayout = QtWidgets.QHBoxLayout()
        # buttons
        self.addToStack = QtWidgets.QPushButton("Add to stack") 
        self.discardFromStack = QtWidgets.QPushButton("Discard from stack")
        self.removeFromStack = QtWidgets.QPushButton("Remove from stack")
        self.removeChannels = QtWidgets.QPushButton("Remove channels")
        self.performRemoval = QtWidgets.QPushButton("Perform Removal")
        self.cancelRemoval = QtWidgets.QPushButton("Cancel Removal")
        self.performPolyFit = QtWidgets.QPushButton("Perform Polyfit")
        self.fitPolynomial = QtWidgets.QPushButton("Fit Polynomial")
        self.automaticReduction = QtWidgets.QPushButton("Go AUTO")
        self.nextScan = QtWidgets.QPushButton("->")
        self.prevScan = QtWidgets.QPushButton("<-")
        self.finishPol = QtWidgets.QPushButton("Finish LHC")
        # buttons placing
        self.nextPrevScanLayout.addWidget(self.prevScan)
        self.nextPrevScanLayout.addWidget(self.nextScan)
        self.vboxMainOperationsFrame.addLayout(self.nextPrevScanLayout)
        self.vboxMainOperationsFrame.addWidget(self.addToStack)
        self.vboxMainOperationsFrame.addWidget(self.discardFromStack)
        self.vboxMainOperationsFrame.addWidget(self.removeFromStack)
        self.vboxMainOperationsFrame.addWidget(self.performPolyFit)
        self.vboxMainOperationsFrame.addWidget(self.performRemoval)
        self.vboxMainOperationsFrame.addWidget(self.cancelRemoval)
        self.vboxMainOperationsFrame.addWidget(self.finishPol)
        self.vboxChannelHandling.addWidget(self.removeChannels)
        self.vboxChannelHandling.addWidget(self.fitPolynomial)
        self.vboxChannelHandling.addWidget(self.automaticReduction)
        
        # buttons sizing
        self.addToStack.setMaximumSize(10000, 10000)
        self.addToStack.setMinimumSize(0, 0)
        self.discardFromStack.setMaximumSize(10000, 10000)
        self.discardFromStack.setMinimumSize(0, 0)
        self.removeFromStack.setMaximumSize(10000, 10000)
        self.removeFromStack.setMinimumSize(0, 0)
        self.removeChannels.setMaximumSize(10000, 10000)
        self.removeChannels.setMinimumSize(0, 0)
        self.fitPolynomial.setMaximumSize(10000, 10000)
        self.fitPolynomial.setMinimumSize(0, 0)
        self.automaticReduction.setMaximumSize(10000, 10000)
        self.automaticReduction.setMinimumSize(0, 0)
        self.finishPol.setMaximumSize(10000, 10000)
        self.finishPol.setMinimumSize(0, 0)
        self.performPolyFit.setMaximumSize(10000, 10000)
        self.performPolyFit.setMinimumSize(0, 0)
        self.performRemoval.setMaximumSize(10000, 10000)
        self.performRemoval.setMinimumSize(0, 0)
        self.cancelRemoval.setMaximumSize(10000, 10000)
        self.cancelRemoval.setMinimumSize(0, 0)

        # buttons colors
        '''
        self.addToStack.setStyleSheet("background-color: green")
        self.discardFromStack.setStyleSheet("background-color: red")
        self.removeFromStack.setStyleSheet("background-color: red")
        self.removeChannels.setStyleSheet("background-color: red")
        self.automaticReduction.setStyleSheet("background-color: blue")
        self.finishPol.setStyleSheet("background-color: blue")
        '''
    
    def __placeNecessaryButtons(self):
        # layouts placing
        self.layout.addWidget(self.mainOperationsFrame, 0,0)
        self.layout.addWidget(self.channelHandlingFrame, 1,0)
        self.layout.addWidget(self.scanFigure, 0, 1, 2,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,5)

    def __defaultSettings(self):
        self.fitPolynomial.setCheckable(True)
        self.removeChannels.setCheckable(True)
        self.automaticReduction.setCheckable(True)
        self.fitPolynomial.setChecked(True)
    
    # ---- clicking and fitting ----
    def __onClick(self, event):
        try:
            x = int(event.xdata)
        except:
            return
        if x is None:
            return
        if self.polyFitMode:
            if self.fitDone:
                self.fitBoundsChannels = []
                self.fitDone = False

            if not self.clickedOnce:
                self.tmpChans.append(x)
                self.clickedOnce = True
            else:
                self.tmpChans.append(x)
                self.fitBoundsChannels.append(self.tmpChans)
                self.tmpChans = []
                self.clickedOnce = False
        
        elif self.removeChannelsMode:
            if self.removeDone:
                self.removeChannelsTab = []
                self.removeDone = False

            if not self.clickedOnce:
                self.tmpChans.append(x)
                self.clickedOnce = True
            else:
                self.tmpChans.append(x)
                self.removeChannelsTab.append(self.tmpChans)
                self.tmpChans = []
                self.clickedOnce = False  

        self.__plotVerticalLine(x)
        

    def __plotVerticalLine(self, x):
        if self.polyFitMode:
            self.scanFigure.axisForScanYZoom.axvline(x, c='lime', ls='--', lw=2)
            self.scanFigure.axisForScanYFull.axvline(x, c='lime', ls='--', lw=2)
        elif self.removeChannelsMode:
            self.scanFigure.axisForScanYZoom.axvline(x, c='coral', ls='--', lw=2)
            self.scanFigure.axisForScanYFull.axvline(x, c='coral', ls='--', lw=2)

        self.scanFigure.figure.canvas.draw_idle()

    def removeLines(self):
        if len(self.scanFigure.axisForScanYZoom.lines) > 2:
            for i in range(len(self.scanFigure.axisForScanYZoom.lines)-1, 1, -1 ):
                self.scanFigure.axisForScanYZoom.lines.remove(self.scanFigure.axisForScanYZoom.lines[i])
            for i in range(len(self.scanFigure.axisForScanYFull.lines)-1, 0, -1 ):
                self.scanFigure.axisForScanYFull.lines.remove(self.scanFigure.axisForScanYFull.lines[i])
    def setFitDone(self):
        self.removeLines()
        self.tmpChans = []
        self.clickedOnce = False
        self.fitDone = True
    
    def setRemoveDone(self):
        self.removeLines()
        self.tmpChans = []
        self.clickedOnce = False
        self.removeDone = True

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