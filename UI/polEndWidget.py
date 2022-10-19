'''
This class holds widget for polarization reduction end
'''


from PySide2 import QtCore, QtWidgets, QtGui
from customButton import cButton
from moreEfficentFigureTemplate import templateFigurePG
import pyqtgraph as pg
from customLeftBarWidget import cWidget

class polEndWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        Initializing the widget
        -> declare figures etc.
        '''
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.newPolEndFig = polEndFigurePG(self)
        self.calCoeffFig = calTabFigure(self)
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

        self.fitBoundChannels = []
        self.tmpChans = []
        self.removeChannelsTab = []

        self.newPolEndFig.pSpec.scene().sigMouseClicked.connect(self.__onClick)

    def plotSpectrum(self, x, y):
        self.newPolEndFig.plotSpectrum(x,y)

    def plotSpectrumWOAutoRange(self, x,y):
        self.newPolEndFig.plotSpecWOAutoRange(x,y)

    def plotCalCoeffsTable(self, x,y):
        self.calCoeffFig.plotCaltab(x,y)
    
    def plotUsedCalCoeff(self, x,y):
        self.calCoeffFig.plotUsedCalCoeff(x,y)

    def __declareNecessaryButtons(self):
        self.leftWidget = cWidget()#QtWidgets.QWidget()
        self.vboxLeftWidget = QtWidgets.QVBoxLayout(self.leftWidget)
        self.vboxLeftWidget.setMargin(0)

        self.vboxStokesFrame = QtWidgets.QVBoxLayout()
        self.stokesFrame = QtWidgets.QGroupBox("Stokes handling")
        self.stokesFrame.setLayout(self.vboxStokesFrame)

        self.vboxDataEditFrame = QtWidgets.QVBoxLayout()
        self.dataEditFrame = QtWidgets.QGroupBox("Data edit")
        self.dataEditFrame.setLayout(self.vboxDataEditFrame)

        self.vboxModesHandling = QtWidgets.QVBoxLayout()
        self.modesHandlingFrame = QtWidgets.QGroupBox("Modes")
        self.modesHandlingFrame.setLayout(self.vboxModesHandling)

        self.vboxCalHandling = QtWidgets.QVBoxLayout()
        self.calHandling = QtWidgets.QGroupBox("Calibration handling")
        self.calHandling.setLayout(self.vboxCalHandling)

        # buttons
        self.goToNextPol = cButton("Go to next Pol") 
        self.backToPol = cButton("Return to scan edit")
        self.cancelCalibrations = cButton("Cancel calibrations")
        self.useCalibrations = cButton("Use calibrations")
        self.setManualCal =  cButton("Set cal coeff manually")

        self.removeChannels = cButton("Remove channels")
        self.fitPolynomial = cButton("Fit Polynomial")
        self.performFit = cButton("Perform Fit")
        self.performRemoval = cButton("Perform removal")
        self.reverseChanges = cButton("Abandon changes")
        self.zoomButton = cButton("Zoom")
        self.setDefaultRangeButton = cButton("Set default range")
        # buttons placing
        self.vboxStokesFrame.addWidget(self.goToNextPol)
        self.vboxStokesFrame.addWidget(self.backToPol)

        self.vboxDataEditFrame.addWidget(self.performFit)
        self.vboxDataEditFrame.addWidget(self.performRemoval)
        self.vboxDataEditFrame.addWidget(self.reverseChanges)
        self.vboxDataEditFrame.addWidget(self.setDefaultRangeButton)

        self.vboxCalHandling.addWidget(self.useCalibrations)
        self.vboxCalHandling.addWidget(self.cancelCalibrations)
        self.vboxCalHandling.addWidget(self.setManualCal)

        self.vboxModesHandling.addWidget(self.fitPolynomial)
        self.vboxModesHandling.addWidget(self.removeChannels)
        self.vboxModesHandling.addWidget( self.zoomButton)

        self.vboxLeftWidget.addWidget(self.stokesFrame)
        self.vboxLeftWidget.addWidget(self.dataEditFrame)
        self.vboxLeftWidget.addWidget(self.modesHandlingFrame)
        self.vboxLeftWidget.addWidget(self.calHandling)

    def __placeNecessaryButtons(self):
        #self.layout.addWidget(self.stokesFrame, 0,0)
        #self.layout.addWidget(self.calHandling, 1,0)
        #self.layout.addWidget(self.dataEditFrame, 2,0)
        #self.layout.addWidget(self.modesHandlingFrame, 3,0)
        self.layout.addWidget(self.leftWidget, 0,0, 4, 1)
        self.layout.addWidget(self.newPolEndFig, 0,1,3,4)
        self.layout.addWidget(self.calCoeffFig, 3,1,1,4)

        [self.layout.setRowStretch(i, 1) for i in range(self.layout.rowCount())]
        [self.layout.setColumnStretch(i, 1) for i in range(self.layout.columnCount())]

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
    @QtCore.Slot()
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
        self.newPolEndFig.pSpec.setMouseEnabled(x=False, y=False)
        print("-----> Polynomial fit mode is ACTIVE!")
    @QtCore.Slot()
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
        self.newPolEndFig.pSpec.setMouseEnabled(x=False, y=False)
        print("-----> Channel removal mode is ACTIVE!")
    @QtCore.Slot()
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
        self.newPolEndFig.pSpec.setMouseEnabled(x=True, y=True)
        print("-----> Zoom mode is ACTIVE!")
    @QtCore.Slot()
    def setDefaultRange(self):
        '''
        This method sets default range of the spectrum plot
        should be attatcheed to the button and shortcut 'b' 
        '''
        self.newPolEndFig.autoRangeSpectrumPlot()

    def __onClick(self, event):
        green = (0,150,0)
        red = (255, 127, 80)
        try:
            mp = self.newPolEndFig.pSpec.vb.mapSceneToView(event.scenePos())
            x = mp.x()
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
            self.newPolEndFig.drawVline(x, green)

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
            self.newPolEndFig.drawVline(x, red)

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
        self.newPolEndFig.clearVlines()

    def setFluxLabel(self, calCoeff):
        if calCoeff == 1:
            self.newPolEndFig.setLabelY("Antenna Temperature (K)")
        else:
            self.newPolEndFig.setLabelY("F = " + str(round(calCoeff,2)) + ' * Ta')

class polEndFigurePG(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setUpNewFigure()
        self.__makeCrossHair()
        
        # -- private
        self.__vlineTab = []

    def __setUpNewFigure(self):
        self.pSpec = self.addPlot()
        self.pSpec.showGrid(x=True, y=True, alpha=0.8)
        cyan = (255,255,255)
        self.spectrumPlot = self.pSpec.plot([0,1], pen=cyan, name="specPlot")
        self.pSpec.setMouseEnabled(x=False, y=False)
        self.pSpec.setLabel(axis='bottom', text="Velocity (km/s)")
        # -
        self.pSpec.scene().setMoveDistance(100)
        # -
        cursor = QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.pSpec.setCursor(cursor)
        # -
        #self.pSpec.vb.autoRange(padding = 0.1, items=[self.spectrumPlot])

    def plotSpectrum(self, x, y):
        self.spectrumPlot.setData(x,y)
        self.pSpec.vb.autoRange(padding=0.05, items=[self.spectrumPlot])
    
    def autoRangeSpectrumPlot(self):
        self.pSpec.vb.autoRange(padding=0.05, items=[self.spectrumPlot])

    def plotSpecWOAutoRange(self, x,y):
        self.spectrumPlot.setData(x,y)
    
    def drawVline(self, pos, wcolor):
        penw = pg.mkPen(color=wcolor, width=3, style=QtCore.Qt.DashLine)
        self.__vlineTab.append(pg.InfiniteLine(pos=pos, angle=90.0, pen=penw))
        self.pSpec.addItem(self.__vlineTab[len(self.__vlineTab)-1] )

    def clearVlines(self):
        [self.pSpec.removeItem(i) for i in self.__vlineTab]
        self.__vlineTab = []
    
    def setLabelY(self, label):
        self.pSpec.setLabel(axis='left', text=label)
    
    def __makeCrossHair(self):
        penw = pg.mkPen(color=(128, 128, 128), width=2)
        self.xCross = pg.InfiniteLine(pos=0.0, angle=90.0, pen=penw)
        self.pSpec.addItem(self.xCross)
        self.pSpec.scene().sigMouseMoved.connect(self.__mouseMovedEvent)

    def __mouseMovedEvent(self, event):
        mp = self.pSpec.vb.mapSceneToView(event)
        x = mp.x()
        self.xCross.setValue(x)

class calTabFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setUpNewFigure()
        #self.setVisible(True)
    def __setUpNewFigure(self):
        self.pCalCoeffs = self.addPlot()
        self.pCalCoeffs.showGrid(x=True, y=True, alpha=0.8)
        # --
        cyan = (255,255,255)
        limePen = (255,0,0)
        # --
        self.caltabPlot = self.pCalCoeffs.plot([0], symbol='+', symbolSize=6, symbolBrush=cyan, pen=None)
        self.usedCalCoeffPlot = self.pCalCoeffs.plot([0], symbol='o', symbolSize=12, symbolBrush=limePen, pen=None)
        # --
        self.pCalCoeffs.setLabel(axis='bottom', text="MJD")
    def plotCaltab(self, x,y):
        self.caltabPlot.setData(x,y)
    
    def plotUsedCalCoeff(self, x,y):
        self.usedCalCoeffPlot.setData([x], [y])