'''
This class holds last widget of them all:
fihishing widget
'''

from PySide2 import QtWidgets
from customButton import cButton
from moreEfficentFigureTemplate import templateFigurePG
from customLeftBarWidget import cWidget

class finishWidgetP(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        #self.fig = finishFigure()
        self.fig = newFinishFigure(self)
        #self.NT = NavigationToolbar(self.fig, self)
        self.__declareButtons()
        self.__placeEv()
    
    def __declareButtons(self):
        self.leftWidget = cWidget()
        self.leftWLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.vboxMainOperationsFrame = QtWidgets.QVBoxLayout()
        self.mainOperatiosFrame = QtWidgets.QGroupBox("Main operations")
        self.mainOperatiosFrame.setLayout(self.vboxMainOperationsFrame)
        # --
        self.endDataReduction = cButton("End data reduction")
        # --
        self.leftWLayout.addWidget(self.mainOperatiosFrame)
        # --
        self.vboxMainOperationsFrame.addWidget(self.endDataReduction)
        # --
        self.endDataReduction.setMaximumSize(10000, 10000)
        self.endDataReduction.setMinimumSize(0, 0)
    
    def __placeEv(self):
        self.layout.addWidget(self.leftWidget, 0,0)
        self.layout.addWidget(self.fig, 0,1)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,5)
    
    def plotPols(self, vels, I, V, LHC, RHC):
        self.fig.plotI.setData(vels, I)
        self.fig.plotV.setData(vels, V)
        self.fig.plotRHC.setData(vels, RHC)
        self.fig.plotLHC.setData(vels, LHC)
    
    def setYlabel(self, label):
        self.fig.setYLabel(label)

class newFinishFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setUpNewFigure()
    
    def __setUpNewFigure(self):
        self.p = self.addPlot()
        self.p.addLegend()
        # --
        white = (255,255,255)
        blue=(100, 100, 255)
        lime = (0,255,0)
        red = (192, 10, 10)
        # --
        self.plotI = self.p.plot([0,1], pen=white, name='I')
        self.plotV = self.p.plot([0,1], pen=blue, name='V')
        self.plotLHC = self.p.plot([0,1], pen=red, name='LHC')
        self.plotRHC = self.p.plot([0,1], pen=lime, name='RHC')
        # --
        self.p.setLabel(axis='bottom', text='Velocity (km/s)')
        # --
        self.p.scene().setMoveDistance(100)

    def setYLabel(self, label):
        self.p.setLabel(axis='left', text=label)
