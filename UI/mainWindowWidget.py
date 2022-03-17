'''
Class, that holds the Main Window of the program
Author: Michał Durjasz
Date: 8.03.2022
'''
from PySide2 import QtCore, QtWidgets, QtGui
from scanStackingWidget import scanStackingWidget, scanStackingFigure
from polEndWidget import polEndWidget
import numpy as np

# -- class definition starts here --
class mainWindowWidget(QtWidgets.QMainWindow):
    # -- init --
    def __init__(self, parent, data = None):
        super().__init__()
        '''
        This is an initialising method. In it, we will place buttons
        and other widgets correctly, by using private methods below:
        Also we will initialize data reduction by plotting data, if we can:
        '''
        self.BBCs = [1,4]
        self.__declareAndPlaceButtons()
        self.__declareAndPlaceCustomWidgets()
        self.__setSomeOtherSettings() # mainly column stretch
        self.__connectButtonsToSlots()
        if data != None:
            self.data = data
            self.actualScanNumber = 0
            self.actualBBC = self.BBCs[0]
            self.actualFitOrder = 10
            self.maximumScanNumber = len(data.obs.mergedScans)
            self.__plotTimeInfo()
            self.__plotScanNo(self.actualScanNumber)
            self.lhcReduction = True
        self.__setPolyFitMode()
    def __declareAndPlaceButtons(self):
        '''
        This methood will declare and place buttons correctly. There
        is also declared layout (QGrid) and primary widget(window), so watch out for that.
        Maybe it would be better to declare it separately?
        Buttons will be placed in the groupBox
        '''
        # layouts
        self.window = QtWidgets.QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QtWidgets.QGridLayout(self.window)

    def __declareAndPlaceCustomWidgets(self):
        self.scanStacker = scanStackingWidget()
        self.polEnd = polEndWidget()
        self.layout.addWidget(self.scanStacker, 0, 1, 2, 1)
    
    def __setSomeOtherSettings(self):
        #self.layout.setColumnStretch(0, 1)
        #self.layout.setColumnStretch(1, 5)
        pass

    def __connectButtonsToSlots(self):
        self.scanStacker.nextScan.clicked.connect(self.__nextScanSlot)
        self.scanStacker.prevScan.clicked.connect(self.__prevScanSlot)
        self.scanStacker.addToStack.clicked.connect(self.__addToStackSlot)
        self.scanStacker.removeFromStack.clicked.connect(self.__deleteFromStackSlot)
        self.scanStacker.finishPol.clicked.connect(self.__finishPol)
        self.scanStacker.fitPolynomial.clicked.connect(self.__setPolyFitMode)
        self.scanStacker.removeChannels.clicked.connect(self.__setRemoveChansMode)
        self.scanStacker.automaticReduction.clicked.connect(self.__setAutoReductionMode)
        self.scanStacker.discardFromStack.clicked.connect(self.__discardScan)
        self.scanStacker.performPolyFit.clicked.connect(self.__fitAndPlot)
        self.scanStacker.performRemoval.clicked.connect(self.__removeAndPlot)
        self.scanStacker.cancelRemoval.clicked.connect(self.__cancelRemoval)

        self.polEnd.performFit.clicked.connect(self.__fitToFinalSpectum)
        self.polEnd.performRemoval.clicked.connect(self.__removeOnFinalSpectrum)
        self.polEnd.reverseChanges.clicked.connect(self.__cancelChangesOnFinalSpectrum)

    def __plotScanNo(self, scanNumber):
        '''
        It plots scan of the number, given in the argument
        WHAT IT DOES:
        -> fits the polynomial (right before plottng)
        -> puts on the graphs:
        --> merged scan
        --> zoomed merged scan + poly fit
        --> resulting spectrum
        -> also marks, which Z, Tsys and Total Flux we are at
        '''
        # ------------
        if scanNumber > len(self.data.obs.mergedScans):
            return
        # ------------
        noOfChannels = len(self.data.obs.mergedScans[scanNumber].pols[0])
        channelTab = np.linspace(1, noOfChannels, noOfChannels)
        self.scanStacker.scanFigure.fullYScanPlot.set_data(channelTab, self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1])
        self.scanStacker.scanFigure.zoomedYScanPlot.set_data(channelTab, self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1])
        # ------------
        if len(self.scanStacker.fitBoundsChannels) != 0:
            self.data.fitBoundsChannels = self.scanStacker.fitBoundsChannels
        #print(self.data.fitBoundsChannels)
        polyTabX, polyTabY, polyTabResiduals = self.data.fitChebyForScan(self.actualBBC, self.actualFitOrder, scanNumber)
        self.scanStacker.scanFigure.fitChebyPlot.set_data(polyTabX, polyTabY)
        self.scanStacker.setFitDone()
        self.scanStacker.scanFigure.spectrumToStackPlot.set_data(range(len(polyTabResiduals)), polyTabResiduals)
        self.scanStacker.setVline(self.data.mergedTimeTab[self.actualScanNumber])
        # --
        stackPlot = self.data.calculateSpectrumFromStack()
        if len(stackPlot) == 1:
            self.scanStacker.scanFigure.stackPlot.set_data(np.nan, np.nan)
        else:
            self.scanStacker.scanFigure.stackPlot.set_data(range(len(stackPlot)), stackPlot)
        # --
        timesDot = [self.data.timeTab[2* self.actualScanNumber], self.data.timeTab[2 * self.actualScanNumber+1]]
        tsysDot = [self.data.tsysTab[self.actualBBC-1][2 * self.actualScanNumber], self.data.tsysTab[self.actualBBC-1][2 * self.actualScanNumber + 1] ]
        totalFluxDot = self.data.totalFluxTab[self.actualBBC-1][self.actualScanNumber]
        zDot = [self.data.zTab[2 * self.actualScanNumber], self.data.zTab[2 * self.actualScanNumber+1] ]
        self.scanStacker.setDots(timesDot, tsysDot, zDot, totalFluxDot )
        self.scanStacker.updateDataPlots()
    
    def __plotTimeInfo(self):
        #print(self.data.timeTab)
        #print(self.data.zTab)
        self.scanStacker.scanFigure.zPlot.set_data(self.data.timeTab, self.data.zTab)
        for i in self.data.tsysTab:
            self.scanStacker.scanFigure.axisForTsys.plot(self.data.timeTab, i, ls="", marker='o', mec='red', mfc="none")
        self.scanStacker.scanFigure.actualTsysPlot.set_data(self.data.timeTab, self.data.tsysTab[self.actualBBC-1])
        self.scanStacker.scanFigure.totalFluxPlot.set_data(self.data.mergedTimeTab, self.data.totalFluxTab[self.actualBBC-1])
        self.scanStacker.updateInfo()

    '''
    Methods below are being used as SLOTS
    '''

    def __nextScanSlot(self):
        if self.actualScanNumber+1 < self.maximumScanNumber:
            self.actualScanNumber += 1
        else:
            self.actualScanNumber = 0
        
        self.__plotScanNo(self.actualScanNumber)
    
    def __prevScanSlot(self):
        if self.actualScanNumber-1 >= 0:
            self.actualScanNumber -= 1
        else:
            self.actualScanNumber = self.maximumScanNumber-1
        
        self.__plotScanNo(self.actualScanNumber)
    
    def __addToStackSlot(self):
        self.data.addToStack(self.actualScanNumber)
        self.__nextScanSlot()
    
    def __deleteFromStackSlot(self):
        self.data.deleteFromStack(self.actualScanNumber)
        self.__plotScanNo(self.actualScanNumber)

    def __finishPol(self):
        # data
        if self.lhcReduction:
            self.data.setLHCTab()
        else:
            self.data.setRHCTab()
        # UI
        self.scanStacker.setVisible(False)
        self.layout.removeWidget(self.scanStacker)
        self.layout.addWidget(self.polEnd, 0, 1, 2, 1)
        self.polEnd.setVisible(True)
        # plot
        if self.lhcReduction:
            spectr = self.data.calculateSpectrumFromStack()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], spectr)
        # BBC
        self.actualBBC = self.BBCs[1]
        # polyfitmode
        self.polEnd.setPolyFitMode()
    
    def __discardScan(self):
        self.__nextScanSlot()

    def __setPolyFitMode(self):
        self.scanStacker.polyFitMode = True
        self.scanStacker.removeChannelsMode = False
        self.scanStacker.autoRedMode = False
        self.scanStacker.fitPolynomial.setChecked(True)
        self.scanStacker.removeChannels.setChecked(False)
        self.scanStacker.automaticReduction.setChecked(False)
        self.scanStacker.performRemoval.setEnabled(False)
        self.scanStacker.performPolyFit.setEnabled(True)
        self.scanStacker.removeLines()
        print("-----> Polynomial fit mode is ACTIVE!")

    def __setRemoveChansMode(self):
        self.scanStacker.polyFitMode = False
        self.scanStacker.removeChannelsMode = True
        self.scanStacker.autoRedMode = False
        self.scanStacker.fitPolynomial.setChecked(False)
        self.scanStacker.removeChannels.setChecked(True)
        self.scanStacker.automaticReduction.setChecked(False)
        self.scanStacker.performRemoval.setEnabled(True)
        self.scanStacker.performPolyFit.setEnabled(False)
        self.scanStacker.removeLines()
        print("-----> Channel removal mode is ACTIVE!")
    
    def __setAutoReductionMode(self):
        self.scanStacker.polyFitMode = False
        self.scanStacker.removeChannelsMode = False
        self.scanStacker.autoRedMode = True
        self.scanStacker.fitPolynomial.setChecked(False)
        self.scanStacker.removeChannels.setChecked(False)
        self.scanStacker.automaticReduction.setChecked(True)
        print("-----> Auto reduction mode is ACTIVE!")
    
    def __fitAndPlot(self):
        self.scanStacker.setFitDone()
        self.__plotScanNo(self.actualScanNumber)
    
    def __removeAndPlot(self):
        self.data.removeChannels(self.actualBBC, self.actualScanNumber, self.scanStacker.removeChannelsTab)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)
    
    def __cancelRemoval(self):
        self.data.cancelRemoval(self.actualBBC, self.actualScanNumber)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)
    
    def __fitToFinalSpectum(self):
        if len(self.polEnd.fitBoundChannels) != 0:
            ftBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.fitBoundChannels)
            self.data.finalFitBoundChannels = ftBds
        self.data.fitChebyToFinalSpec(self.actualBBC)
        # -- 
        self.polEnd.setFitDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)
    
    def __removeOnFinalSpectrum(self):
        if (len(self.polEnd.removeChannelsTab)) != 0:
            rmBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.removeChannelsTab)
            self.data.removeChansOnFinalSpectrum(rmBds)
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)
    
    def __cancelChangesOnFinalSpectrum(self):
        self.data.cancelChangesFinal()
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)