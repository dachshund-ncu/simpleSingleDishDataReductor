'''
Class, that holds the Main Window of the program
Author: Michał Durjasz
Date: 8.03.2022
'''
from PySide2 import QtCore, QtWidgets, QtGui
from scanStackingWidget import scanStackingWidget, scanStackingFigure
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
        self.__declareAndPlaceButtons()
        self.__declareAndPlaceCustomWidgets()
        self.__setSomeOtherSettings() # mainly column stretch
        if data != None:
            self.data = data
            self.actualScanNumber = 0
            self.__plotScanNo(self.actualScanNumber)

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
        # buttons
        self.addToStack = QtWidgets.QPushButton("Add to stack") 
        self.discardFromStack = QtWidgets.QPushButton("Discard from stack")
        self.removeFromStack = QtWidgets.QPushButton("Remove from stack")
        self.removeChannels = QtWidgets.QPushButton("Remove channels")
        self.fitPolynomial = QtWidgets.QPushButton("Fit Polynomial")
        self.automaticReduction = QtWidgets.QPushButton("Go AUTO")
        # buttons placing
        self.vboxMainOperationsFrame.addWidget(self.addToStack)
        self.vboxMainOperationsFrame.addWidget(self.discardFromStack)
        self.vboxMainOperationsFrame.addWidget(self.removeFromStack)
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
        # buttons colors
        self.addToStack.setStyleSheet("background-color: green")
        self.discardFromStack.setStyleSheet("background-color: red")
        self.removeFromStack.setStyleSheet("background-color: red")
        self.removeChannels.setStyleSheet("background-color: red")
        self.automaticReduction.setStyleSheet("background-color: blue")
    
    def __declareAndPlaceCustomWidgets(self):
        self.scanStacker = scanStackingWidget()
        self.layout.addWidget(self.scanStacker, 0, 1, 2, 1)
    
    def __setSomeOtherSettings(self):
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 5)
    
    def __plotFirstScan(self, data):
        length = len(data.obs.mergedScans[0].pols[0])
        x = np.linspace(1, length, length)
        self.scanStacker.scanFigure.axisForScanYFull.plot(x, data.obs.mergedScans[0].pols[0])
    
    def __plotScanNo(self, scanNumber):
        noOfChannels = len(self.data.obs.mergedScans[scanNumber].pols[0])
        channelTab = np.linspace(1, noOfChannels, noOfChannels)
        self.scanStacker.scanFigure.axisForScanYFull.plot(channelTab, self.data.obs.mergedScans[scanNumber].pols[0])
        self.scanStacker.scanFigure.axisForScanYZoom.plot(channelTab, self.data.obs.mergedScans[scanNumber].pols[0])