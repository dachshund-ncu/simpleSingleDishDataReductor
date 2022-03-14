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
        self.vboxMainOperationsFrame.addWidget(self.finishPol)
        self.vboxChannelHandling.addWidget(self.removeChannels)
        self.vboxChannelHandling.addWidget(self.fitPolynomial)
        self.vboxChannelHandling.addWidget(self.automaticReduction)
        # layouts placing
        self.layout.addWidget(self.mainOperationsFrame, 0,0)
        self.layout.addWidget(self.channelHandlingFrame, 1,0)
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
        # buttons colors
        self.addToStack.setStyleSheet("background-color: green")
        self.discardFromStack.setStyleSheet("background-color: red")
        self.removeFromStack.setStyleSheet("background-color: red")
        self.removeChannels.setStyleSheet("background-color: red")
        self.automaticReduction.setStyleSheet("background-color: blue")
        self.finishPol.setStyleSheet("background-color: blue")
    
    def __declareAndPlaceCustomWidgets(self):
        self.scanStacker = scanStackingWidget()
        self.polEnd = polEndWidget()
        self.layout.addWidget(self.scanStacker, 0, 1, 2, 1)
    
    def __setSomeOtherSettings(self):
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 5)
    
    def __connectButtonsToSlots(self):
        self.nextScan.clicked.connect(self.__nextScanSlot)
        self.prevScan.clicked.connect(self.__prevScanSlot)
        self.addToStack.clicked.connect(self.__addToStackSlot)
        self.removeFromStack.clicked.connect(self.__deleteFromStackSlot)
        self.finishPol.clicked.connect(self.__finishPol)

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
        polyTabX, polyTabY, polyTabResiduals = self.data.fitChebyForScan(self.actualBBC, self.actualFitOrder, scanNumber)
        self.scanStacker.scanFigure.fitChebyPlot.set_data(polyTabX, polyTabY)
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
        if self.actualScanNumber-1 > 0:
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
            spectr = self.data.LHCTab
        else:
            spectr = self.data.LHCTab
        self.polEnd.plotSpectrum(range(len(spectr)), spectr)
        # BBC
        self.actualBBC = self.BBCs[1]