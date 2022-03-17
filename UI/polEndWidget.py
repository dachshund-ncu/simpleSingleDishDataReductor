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
        self.__declareNecessaryButtons()
        self.__placeNecessaryButtons()
        self.__setOtherBeginnerSettings()

        self.polyFitMode = True
        self.removeChannelsMode = False
        self.zoomMode = False

        self.__connectButtonsToSlots()

        # -- channel selector --
        self.fitDone = True
        self.removeDone = True
        self.zoomDone = True
        self.clickedOnce = False

        self.fitBoundChannels = [
            [10,20],
            [1100, 2038]
        ]
        self.tmpChans = []
        self.removeChannelsTab = []


        id = self.polEndFIg.figure.canvas.mpl_connect('button_press_event', self.__onClick)

    def plotSpectrum(self, x, y):
        self.polEndFIg.plotSpectrum(x,y)

    def __declareNecessaryButtons(self):
        self.vboxMainOperationsFrame = QtWidgets.QVBoxLayout()
        self.mainOperationsFrame = QtWidgets.QGroupBox("Main operations")
        self.mainOperationsFrame.setLayout(self.vboxMainOperationsFrame)

        self.vboxCalOpsFrame = QtWidgets.QVBoxLayout()
        self.calOpsFrame = QtWidgets.QGroupBox("Calibration")
        self.calOpsFrame.setLayout(self.vboxCalOpsFrame)

        self.vboxModesHandling = QtWidgets.QVBoxLayout()
        self.modesHandlingFrame = QtWidgets.QGroupBox("modes")
        self.modesHandlingFrame.setLayout(self.vboxModesHandling)
        # buttons
        self.goToNextPol = QtWidgets.QPushButton("Finish LHC") 
        self.backToPol = QtWidgets.QPushButton("Return to LHC")
        self.cancelCalibrations = QtWidgets.QPushButton("Cancel calibrations")
        self.useCalibrations = QtWidgets.QPushButton("Use calibrations")
        self.setManualCal =  QtWidgets.QPushButton("Set cal coeff manually")
        self.restoreRemovedChannels = QtWidgets.QPushButton("Restore Removed Channels")

        self.removeChannels = QtWidgets.QPushButton("Remove channels")
        self.fitPolynomial = QtWidgets.QPushButton("Fit Polynomial")
        self.performFit = QtWidgets.QPushButton("Perform Fit")
        self.performRemoval = QtWidgets.QPushButton("Perform removal")
        self.reverseChanges = QtWidgets.QPushButton("Abandon changes")
        self.zoomButton = QtWidgets.QPushButton("Zoom")
        # buttons placing
        self.vboxMainOperationsFrame.addWidget(self.goToNextPol)
        self.vboxMainOperationsFrame.addWidget(self.backToPol)
        self.vboxMainOperationsFrame.addWidget(self.restoreRemovedChannels)
        self.vboxMainOperationsFrame.addWidget(self.performFit)
        self.vboxMainOperationsFrame.addWidget(self.performRemoval)
        self.vboxMainOperationsFrame.addWidget(self.reverseChanges)

        self.vboxCalOpsFrame.addWidget(self.useCalibrations)
        self.vboxCalOpsFrame.addWidget(self.cancelCalibrations)
        self.vboxCalOpsFrame.addWidget(self.setManualCal)
        

        self.vboxModesHandling.addWidget(self.fitPolynomial)
        self.vboxModesHandling.addWidget(self.removeChannels)
        self.vboxModesHandling.addWidget( self.zoomButton)
        
        # buttons sizing
        self.zoomButton.setMaximumSize(10000, 10000)
        self.zoomButton.setMinimumSize(0, 0)
        self.setManualCal.setMaximumSize(10000, 10000)
        self.setManualCal.setMinimumSize(0, 0)
        self.goToNextPol.setMaximumSize(10000, 10000)
        self.goToNextPol.setMinimumSize(0, 0)
        self.backToPol.setMaximumSize(10000, 10000)
        self.backToPol.setMinimumSize(0, 0)
        self.cancelCalibrations.setMaximumSize(10000, 10000)
        self.cancelCalibrations.setMinimumSize(0, 0)
        self.removeChannels.setMaximumSize(10000, 10000)
        self.removeChannels.setMinimumSize(0, 0)
        self.fitPolynomial.setMaximumSize(10000, 10000)
        self.fitPolynomial.setMinimumSize(0, 0)
        self.useCalibrations.setMaximumSize(10000, 10000)
        self.useCalibrations.setMinimumSize(0, 0)
        self.restoreRemovedChannels.setMaximumSize(10000, 10000)
        self.restoreRemovedChannels.setMinimumSize(0, 0)
        self.performFit.setMaximumSize(10000, 10000)
        self.performFit.setMinimumSize(0, 0)
        self.performRemoval.setMaximumSize(10000, 10000)
        self.performRemoval.setMinimumSize(0, 0)
        self.reverseChanges.setMaximumSize(10000, 10000)
        self.reverseChanges.setMinimumSize(0, 0)
        # buttons colors
        '''
        self.goToNextPol.setStyleSheet("background-color: green")
        self.backToPol.setStyleSheet("background-color: red")
        self.cancelCalibrations.setStyleSheet("background-color: red")
        self.useCalibrations.setStyleSheet("background-color: blue")
        self.restoreRemovedChannels.setStyleSheet("background-color: blue")
        self.fitPolynomial.setStyleSheet("background-color: green")
        self.removeChannels.setStyleSheet("background-color: red")
        self.zoomButton.setStyleSheet("background-color: blue")
        '''
    def __placeNecessaryButtons(self):
        self.layout.addWidget(self.mainOperationsFrame, 0,0)
        self.layout.addWidget(self.calOpsFrame, 1,0)
        self.layout.addWidget(self.modesHandlingFrame, 2,0)
        self.layout.addWidget(self.polEndFIg, 0,1,3,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,5)

    def __setOtherBeginnerSettings(self):
        # --
        self.fitPolynomial.setCheckable(True)
        self.removeChannels.setCheckable(True)
        self.zoomButton.setCheckable(True)

    def __connectButtonsToSlots(self):
        self.fitPolynomial.clicked.connect(self.setPolyFitMode)
        self.removeChannels.clicked.connect(self.setRemoveChansMode)
        self.zoomButton.clicked.connect(self.setZoomMode)
    '''
    PRIVATE SLOTS:
    '''
    def setPolyFitMode(self):
        self.polyFitMode = True
        self.removeChannelsMode = False
        self.zoomMode = False
        self.fitPolynomial.setChecked(True)
        self.removeChannels.setChecked(False)
        self.zoomButton.setChecked(False)
        self.setFitDone()
        self.performRemoval.setEnabled(False)
        self.performFit.setEnabled(True)
        print("-----> Polynomial fit mode is ACTIVE!")
    def setRemoveChansMode(self):
        self.polyFitMode = False
        self.removeChannelsMode = True
        self.zoomMode = False
        self.fitPolynomial.setChecked(False)
        self.removeChannels.setChecked(True)
        self.zoomButton.setChecked(False)
        self.setRemoveDone()
        self.performRemoval.setEnabled(True)
        self.performFit.setEnabled(False)
        print("-----> Channel removal mode is ACTIVE!")
    def setZoomMode(self):
        self.polyFitMode = False
        self.removeChannelsMode = False
        self.zoomMode = True
        self.fitPolynomial.setChecked(False)
        self.removeChannels.setChecked(False)
        self.zoomButton.setChecked(True)
        self.setZoomDone()
        self.performRemoval.setEnabled(False)
        self.performFit.setEnabled(False)        
        print("-----> Channel removal mode is ACTIVE!")

    def __onClick(self, event):
        try:
            x = event.xdata
        except:
            return
        if self.polyFitMode:
            if self.fitDone:
                self.fitBoundChannels = []
                self.fitDone = False
            
            if not self.clickedOnce:
                self.tmpChans.append(x)
                self.clickedOnce = True
            else:
                self.tmpChans.append(x)
                self.fitBoundChannels.append(self.tmpChans)
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
                self.clicedOnce = False
        self.__plotVerticalLine(x)

    def __plotVerticalLine(self, x):
        if self.polyFitMode:
            self.polEndFIg.specAxis.axvline(x, c='lime', ls='--')
        elif self.removeChannelsMode:
            self.polEndFIg.specAxis.axvline(x, c='coral', ls='--')
        elif self.zoomMode:
            self.polEndFIg.specAxis.axvline(x, c='blue', ls='--')
        self.polEndFIg.figure.canvas.draw_idle()

    def __resetClickable(self):
        self.removeLines()
        self.tmpChans = []
        self.clickedOnce = False

    def setFitDone(self):
        self.__resetClickable()
        self.fitDone = True
    def setRemoveDone(self):
        self.__resetClickable()
        self.removeDone = True
    def setZoomDone(self):
        self.__resetClickable()
        self.zoomDone = True

    def removeLines(self):
        if len(self.polEndFIg.specAxis.lines) > 1:
            for i in range(len(self.polEndFIg.specAxis.lines)-1, 0, -1):
                self.polEndFIg.specAxis.lines.remove(self.polEndFIg.specAxis.lines[i])

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