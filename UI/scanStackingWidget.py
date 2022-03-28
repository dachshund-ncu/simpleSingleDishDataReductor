'''
Class, that holds the scan stacking widget:
-> plotting actual scans
-> plotting stacked spectrum 
-> plotting z(t), tsys(t), total flux(t)
-> labels: scans, tsys, rms, snr, peak
'''

from PySide2 import QtCore, QtWidgets, QtGui
from customButton import cButton
from abstractFigureClass import templateFigure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
import numpy as np
from moreEfficentFigureTemplate import templateFigurePG
import pyqtgraph as pg

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
        self.newScanFigure = newScanStackingFigure()
        self.newStackedFigure = stackedSpectrumFigure()
        self.newOtherPropsFigure = otherPropsFigure()
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
        self.newScanFigure.drawData()

    def updateInfo(self):
        self.scanFigure.drawInfo()

    def setVline(self, time, ):
        self.scanFigure.tsysVline.set_data([time, time], [0,1])
        self.scanFigure.zVline.set_data([time, time], [0,1])
        self.scanFigure.totalFluxVline.set_data([time, time], [0,1])
        # --
        self.newOtherPropsFigure.tsysVline.setValue(time)
        self.newOtherPropsFigure.totalFluxVline.setValue(time)
    
    def setDots(self, time, ampTsys, zDot, totalFluxDot ):
        self.scanFigure.dot1Tsys.set_data(time[0], ampTsys[0])
        self.scanFigure.dot2Tsys.set_data(time[1], ampTsys[1])
        self.scanFigure.dot1Z.set_data(time[0], zDot[0])
        self.scanFigure.dot2Z.set_data(time[1], zDot[1])
        self.scanFigure.dotTF.set_data(time[1], totalFluxDot)
        # --
        self.newOtherPropsFigure.dot1Tsys.setData([time[0]], [ampTsys[0]])
        self.newOtherPropsFigure.dot2Tsys.setData([time[1]], [ampTsys[1]])
        self.newOtherPropsFigure.dotTF.setData([time[1]], [totalFluxDot])
    
    def __declareNecessaryButtons(self):
        self.leftWidget = QtWidgets.QWidget()
        self.vboxLeftWidget = QtWidgets.QVBoxLayout(self.leftWidget)
        self.vboxLeftWidget.setMargin(0)
        self.vboxScanOperationsFrame = QtWidgets.QVBoxLayout()
        self.ScanOperationsFrame = QtWidgets.QGroupBox("Scan operations")
        self.ScanOperationsFrame.setLayout(self.vboxScanOperationsFrame)

        self.vboxOtherOperationsFrame = QtWidgets.QVBoxLayout()
        self.otherOperationsFrame = QtWidgets.QGroupBox("Other operations")
        self.otherOperationsFrame.setLayout(self.vboxOtherOperationsFrame)

        self.vboxModesFrame = QtWidgets.QVBoxLayout()
        self.modesFrame = QtWidgets.QGroupBox("Modes")
        self.modesFrame.setLayout(self.vboxModesFrame)

        self.nextPrevScanLayout = QtWidgets.QHBoxLayout()
        # buttons
        self.addToStack = cButton("Add to stack") 
        self.discardFromStack = cButton("Discard from stack")
        self.removeFromStack = cButton("Remove from stack")
        self.removeChannels = cButton("Remove channels")
        self.performRemoval = cButton("Perform Removal")
        self.cancelRemoval = cButton("Cancel Removal")
        self.performPolyFit = cButton("Perform Polyfit")
        self.fitPolynomial = cButton("Fit Polynomial")
        self.automaticReduction = cButton("Go AUTO")
        self.nextScan = cButton("->")
        self.prevScan = cButton("<-")
        self.finishPol = cButton("Finish LHC")
        # buttons placing
        self.nextPrevScanLayout.addWidget(self.prevScan)
        self.nextPrevScanLayout.addWidget(self.nextScan)
        self.vboxScanOperationsFrame.addLayout(self.nextPrevScanLayout)
        self.vboxScanOperationsFrame.addWidget(self.addToStack)
        self.vboxScanOperationsFrame.addWidget(self.discardFromStack)
        self.vboxScanOperationsFrame.addWidget(self.removeFromStack)

        self.vboxOtherOperationsFrame.addWidget(self.performPolyFit)
        self.vboxOtherOperationsFrame.addWidget(self.performRemoval)
        self.vboxOtherOperationsFrame.addWidget(self.cancelRemoval)
        self.vboxOtherOperationsFrame.addWidget(self.finishPol)
        
        self.vboxModesFrame.addWidget(self.removeChannels)
        self.vboxModesFrame.addWidget(self.fitPolynomial)
        self.vboxModesFrame.addWidget(self.automaticReduction)

        self.vboxLeftWidget.addWidget(self.ScanOperationsFrame)
        self.vboxLeftWidget.addWidget(self.otherOperationsFrame)
        self.vboxLeftWidget.addWidget(self.modesFrame)
    
    def __placeNecessaryButtons(self):
        # layouts placing
        #self.layout.addWidget(self.ScanOperationsFrame, 0,0)
        #self.layout.addWidget(self.otherOperationsFrame, 1,0, 2, 1)
        #self.layout.addWidget(self.modesFrame, 3,0)
        #self.layout.addWidget(self.scanFigure, 0, 1, 3,1)
        self.layout.addWidget(self.leftWidget, 0, 0, 3, 1)
        self.layout.addWidget(self.newScanFigure, 0, 1, 2,1)
        self.layout.addWidget(self.newStackedFigure, 2, 1, 1, 1)
        self.layout.addWidget(self.newOtherPropsFigure, 0, 2, 2, 1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,3)
        self.layout.setColumnStretch(2,2)

        [self.layout.setRowStretch(i, 1) for i in range(self.layout.rowCount())]

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

class scanStackingFigure(templateFigure):
    def __init__(self):
        super().__init__()
        self.__declareNecessaryWidgets()
        plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95)
        #plt.ion()

    def __declareNecessaryWidgets(self):
        '''
        Will declare the necessary figures and axes.
        Then place them correctly inside the widget
        '''
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
        self.clearPlottable(self.axisForScan)
        self.clearPlottable(self.axisForOthers)
        self.makeFancyTicks(self.axisForStackedSpectrum)
        self.makeFancyTicks(self.axisForScanYFull)
        self.makeFancyTicks(self.axisForScanYZoom)
        self.makeFancyTicks(self.axisForZ)
        self.makeFancyTicks(self.axisForTsys)
        self.makeFancyTicks(self.axisForTotalFlux)

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
        self.autoscaleAxis(self.axisForScanYFull, tight=True)
        self.autoscaleAxis(self.axisForScanYZoom, tight=True)
        self.__autoscaleZoomedPlotY()
        self.autoscaleAxis(self.axisForStackedSpectrum, tight=True)

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
    
class newScanStackingFigure(templateFigurePG):
    def __init__(self):
        super().__init__()
        self.__setUpNewFigure()

    def __setUpNewFigure(self):
        #self.newScanFigure()
        self.pTop = self.addPlot(name='TopPlot')
        self.nextRow()
        self.pZoom = self.addPlot(name='ZoomPlot')
        self.pTop.setXLink(self.pZoom)
        # -
        self.pTop.showGrid(x=True, y=True, alpha=0.8)
        self.pZoom.showGrid(x=True, y=True, alpha=0.8)
        # PENS 
        cyan = (0,255,255)
        red = (255, 127, 80)
        # --
        self.fullYScanPlot = self.pTop.plot([0,1], pen=cyan)
        self.zoomedYScanPlot = self.pZoom.plot([0,1], pen=cyan)
        self.fitChebyPlot = self.pZoom.plot([0,1], pen=pg.mkPen(red, width=2))

        #self.pTop.autoRange(padding=0.0)
        #self.pZoom.autoRange(padding=0.0)

    def __autoscaleZoomedPlotY(self):
        '''
        we need to define our own methood for autoscaling
        the zoomedYScanPlot, because we want it zoomed ;)
        '''
        x,y = self.fitChebyPlot.getData()
        max = y.max()
        min = y.min()
        diff = max-min
        lowerEnd = min - 2.0 * diff
        upperEnd = max + 2.0 * diff
        self.pZoom.setYRange(lowerEnd, upperEnd)
    
    def drawData(self):
        self.__autoscaleZoomedPlotY()

class stackedSpectrumFigure(templateFigurePG):
    def __init__(self):
        super().__init__()
        self.__setUpNewFigure()

    def __setUpNewFigure(self):
        #self.newScanFigure()
        self.p = self.addPlot(name='Stacked Plot')
        # --
        self.p.showGrid(x=True, y=True, alpha=0.8)
        # --
        orange = (255,165,0)
        silver = (128,128,128)
        self.spectrumToStackPlot = self.p.plot([0,1], pen=silver)
        self.stackPlot = self.p.plot([0,1], pen=orange)

class otherPropsFigure(templateFigurePG):
    def __init__(self):
        super().__init__()
        self.__setUpNewFigure()

    def __setUpNewFigure(self):
        self.pTSys = self.addPlot(name='tsysPlot')
        self.nextRow()
        self.pTotal = self.addPlot(name='totalPlot')
        self.pTSys.setXLink(self.pTotal)
        # - 
        self.pTSys.showGrid(x=True, y=True, alpha=0.8)
        self.pTotal.showGrid(x=True, y=True, alpha=0.8)
        # ---
        # ---
        blue=(100, 100, 255)
        lime = (0,255,0)
        magenta = (255, 0, 255)
        self.tsysPlot = self.pTSys.plot([0,1], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        self.actualTsysPlot = self.pTSys.plot([0,1], symbol='o', symbolSize=6, symbolBrush=lime, pen=None)
        self.totalFluxPlot = self.pTotal.plot([0,1], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        # dots
        self.dot1Tsys = self.pTSys.plot( [0,1], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        self.dot2Tsys = self.pTSys.plot( [0,1], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        self.dotTF = self.pTotal.plot([0,1], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        # lines

        self.tsysVline = pg.InfiniteLine(pos=0.0, angle=90.0, pen=magenta)
        self.totalFluxVline = pg.InfiniteLine(pos=0.0, angle=90.0, pen=magenta)
        self.pTSys.addItem(self.tsysVline)
        self.pTotal.addItem(self.totalFluxVline)
        '''
        self.zPlot, = self.axisForZ.plot(np.nan, np.nan, c='blue', ls="", marker='s')
        #self.tsysPlot, = self.axisForTsys.plot(np.nan, np.nan, c='blue', ls="", marker='o', mec='red', mfc="none")
        self.actualTsysPlot, = self.axisForTsys.plot(np.nan, np.nan, c='lime', ls="", marker='o', ms=6, zorder=2)
        self.totalFluxPlot, = self.axisForTotalFlux.plot(np.nan, np.nan, c='cyan', ls="", marker='o', ms=3)
        '''