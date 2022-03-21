'''
This class holds widget for polarization reduction end
'''


from PySide2 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
import numpy as np
from customButton import cButton
from abstractFigureClass import templateFigure


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
        self.goToNextPol = cButton("Go to next Pol") 
        self.backToPol = cButton("Return to scan edit")
        self.cancelCalibrations = cButton("Cancel calibrations")
        self.useCalibrations = cButton("Use calibrations")
        self.setManualCal =  cButton("Set cal coeff manually")
        self.restoreRemovedChannels = cButton("Restore Removed Channels")

        self.removeChannels = cButton("Remove channels")
        self.fitPolynomial = cButton("Fit Polynomial")
        self.performFit = cButton("Perform Fit")
        self.performRemoval = cButton("Perform removal")
        self.reverseChanges = cButton("Abandon changes")
        self.zoomButton = cButton("Zoom")
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

    def __placeNecessaryButtons(self):
        self.layout.addWidget(self.mainOperationsFrame, 0,0)
        self.layout.addWidget(self.calOpsFrame, 1,0)
        self.layout.addWidget(self.modesHandlingFrame, 2,0)
        self.layout.addWidget(self.polEndFIg, 0,1,3,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,5)

    def __setOtherBeginnerSettings(self):
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
        if x is None:
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
                self.clickedOnce = False

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

class polEndFigure(templateFigure):
    def __init__(self):
        super().__init__()
        self.__declareNecessaryWidgets()
        plt.subplots_adjust(top=0.98, bottom=0.08, left=0.08, right=0.98)
    
    def __declareNecessaryWidgets(self):
        self.gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
        self.specAxis = self.figure.add_subplot(self.gs[0,0])
        self.caltabPlot = self.figure.add_subplot(self.gs[1,0])

        self.makeFancyTicks(self.specAxis)
        self.makeFancyTicks(self.caltabPlot)

        self.spectrumPlot, = self.specAxis.plot(np.nan, np.nan, c='cyan', lw=1)
        self.specAxis.set_ylabel("Amplitude")
        self.specAxis.set_xlabel(r"V$_{\mathrm{lsr}}\,$(km$\,$s$^{-1}$)")
        self.caltabPlot.set_xlabel("MJD")
        self.caltabPlot.set_ylabel("Cal coeff.")
    
    def plotSpectrum(self, x,y):
        self.spectrumPlot.set_data(x,y)
        self.autoscaleAxis(self.specAxis, tight=True)
        self.drawF()