'''
This class holds last widget of them all:
fihishing widget
'''

from PySide2 import QtWidgets
from abstractFigureClass import templateFigure
import matplotlib.pyplot as plt
import numpy as np
from customButton import cButton

class finishWidgetP(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.fig = finishFigure()
        self.__declareButtons()
        self.__placeEv()
    
    def __declareButtons(self):
        self.vboxMainOperationsFrame = QtWidgets.QVBoxLayout()
        self.mainOperatiosFrame = QtWidgets.QGroupBox("Main operations")
        self.mainOperatiosFrame.setLayout(self.vboxMainOperationsFrame)
        # --
        self.endDataReduction = cButton("End data reduction")
        # --
        self.vboxMainOperationsFrame.addWidget(self.endDataReduction)
        # --
        self.endDataReduction.setMaximumSize(10000, 10000)
        self.endDataReduction.setMinimumSize(0, 0)
    
    def __placeEv(self):
        self.layout.addWidget(self.mainOperatiosFrame, 0,0)
        self.layout.addWidget(self.fig, 0,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,5)
    
    def plotPols(self, vels, I, V, LHC, RHC):
        self.fig.plotI.set_data(vels, I)
        self.fig.plotV.set_data(vels, V)
        self.fig.plotRHC.set_data(vels, RHC)
        self.fig.plotLHC.set_data(vels, LHC)
        self.fig.autoscaleAxis(self.fig.ax, tight=True)
        self.fig.drawF()

class finishFigure(templateFigure):
    def __init__(self):
        super().__init__()
        self.__declareAxesAndPlots()
    
    def __declareAxesAndPlots(self):
        # ax
        self.ax = self.figure.add_subplot(111)
        # plots
        self.plotI, = self.ax.plot(np.nan, np.nan, c='white', lw=1, label = 'I')
        self.plotV, = self.ax.plot(np.nan, np.nan, c='blue', lw=1, label = 'V')
        self.plotLHC, = self.ax.plot(np.nan, np.nan, c='coral', lw=1, label = 'LHC')
        self.plotRHC, = self.ax.plot(np.nan, np.nan, c='lime', lw=1, label = 'RHC')
        # legend
        self.ax.legend()
        # fancy
        self.makeFancyTicks(self.ax)
