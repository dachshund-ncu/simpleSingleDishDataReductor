'''
Class, that holds the scan stacking widget:
-> plotting actual scans
-> plotting stacked spectrum 
-> plotting z(t), tsys(t), total flux(t)
-> labels: scans, tsys, rms, snr, peak
'''

#from tkinter import Y
from PySide2 import QtCore, QtWidgets, QtGui
from customButton import cButton
from moreEfficentFigureTemplate import templateFigurePG
import pyqtgraph as pg
from customLeftBarWidget import cWidget

class scanStackingWidget(QtWidgets.QWidget):
    def __init__(self):
        '''
        initializing the widget:
        -> will initialize the layout
        -> will declare necessary widgets and place them correctly
        '''
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.newScanFigure = newScanStackingFigure(self)
        self.newStackedFigure = stackedSpectrumFigure(self)
        self.newOtherPropsFigure = otherPropsFigure(self)
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
        
        self.newScanFigure.pTop.scene().sigMouseClicked.connect(self.__onClick)
        self.newOtherPropsFigure.pTotal.scene().sigMouseClicked.connect(self.__onClickAuto)
        # -- for auto threshold --
        self.autoThreshold = -1e11
        self.setVisible(True)

    def updateDataPlots(self):
        self.newScanFigure.drawData()

    def setVline(self, time, ):
        # --
        self.newOtherPropsFigure.tsysVline.setValue(time)
        self.newOtherPropsFigure.totalFluxVline.setValue(time)
    
    def setDots(self, time, ampTsys, zDot, totalFluxDot ):
        # --
        self.newOtherPropsFigure.dot1Tsys.setData([time[0]], [ampTsys[0]])
        self.newOtherPropsFigure.dot2Tsys.setData([time[1]], [ampTsys[1]])
        self.newOtherPropsFigure.dotTF.setData([time[1]], [totalFluxDot])
    
    def __declareNecessaryButtons(self):
        self.leftWidget = cWidget()#QtWidgets.QWidget()
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
        # labels
        # -- scan properties --
        self.grid_labels = QtWidgets.QGridLayout() # grid for labels
        self.props_labels = [QtWidgets.QLabel(f"label {i}") for i in range(10)]
        font = QtGui.QFont("Arial", 12)
        [self.props_labels[i].setFont(font) for i in range(len(self.props_labels))]
        # -- BBC --
        self.bbc_labels = [QtWidgets.QLabel(f"label {i}") for i in range(8)]
        [self.bbc_labels[i].setFont(font) for i in range(len(self.bbc_labels))]


        # labels placing
        for i in range(len(self.props_labels)):
            self.grid_labels.addWidget(self.props_labels[i], int(i/2), int(i%2))
        
        for i in range(len(self.bbc_labels)):
            self.grid_labels.addWidget(self.bbc_labels[i], int(i/2) + 5, int(i%2))

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
        self.layout.addWidget(self.leftWidget, 0, 0, 3, 1)
        self.layout.addWidget(self.newScanFigure, 0, 1, 2,1)
        self.layout.addWidget(self.newStackedFigure, 2, 1, 1, 1)
        self.layout.addWidget(self.newOtherPropsFigure, 0, 2, 2, 1)
        self.layout.addLayout(self.grid_labels, 2,2, 1,1)
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
            mp = self.newScanFigure.pTop.vb.mapSceneToView(event.scenePos())
            x = int(mp.x())
        except:
            return
        if x is None:
            return
        self.__makeAfterClickActionOnSpectrumPlot(x)
        
    def __onClickAuto(self, event):
        if self.autoRedMode:
            mp = self.newOtherPropsFigure.pTotal.vb.mapSceneToView(event.scenePos())
            self.__makeAfterClickActionOnAutoPlot(mp.y())

    def __makeAfterClickActionOnSpectrumPlot(self, x):
        green = (0, 150, 0)
        red = (255, 127, 80)
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
            self.newScanFigure.drawVline(x, green)

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
            self.newScanFigure.drawVline(x, red)

    def __makeAfterClickActionOnAutoPlot(self, y):
            self.autoThreshold = y
            self.newOtherPropsFigure.colorizePoints(self.autoThreshold)


    def removeLines(self):
        self.newScanFigure.clearVlines()

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
    
    def setBoundChannels(self, bChns):
        self.fitBoundsChannels = bChns
    
    def resetRemoveChans(self):
        self.removeChannelsTab = []

    def setLabel(self, mode, polyOrder, fitRms, scanNo, scanMax, SNR, TSys, BBC_number):
        '''
        Simple sets label accordong to scan properties
        TODO: refactoring needed!!!
        '''

        if fitRms > 999999.0:
            fitRms = 'inf'

        for i in range(len(TSys)):
            if TSys[i] > 1000.0:
                TSys[i] = 1000.0
        # --- properties ---
        self.props_labels[0].setText('Mode:')
        self.props_labels[1].setText(mode)
        self.props_labels[2].setText('Scan:')
        self.props_labels[3].setText(str(int(scanNo)) + ' / ' + str(int(scanMax)))
        self.props_labels[4].setText('Polyn. fit order:')
        self.props_labels[5].setText(str(int(polyOrder)))
        self.props_labels[6].setText('Fit RMS:')
        self.props_labels[7].setText(str(fitRms))
        self.props_labels[8].setText('Signal-to-noise ratio:')
        self.props_labels[9].setText(str(SNR))

        # --- bbc ---
        BBC_n = BBC_number-1 # convert to array indice 
        font_chosen = QtGui.QFont("Arial", 12, QtGui.QFont.Bold)
        font_not_chosen = QtGui.QFont("Arial", 12)
        indices = [int(BBC_n*2), int(BBC_n*2) + 1]

        for i in range(len(self.bbc_labels)):
            if i%2 == 0:
                self.bbc_labels[i].setText(f"BBC {int(i/2)+1}")
            else:
                self.bbc_labels[i].setText(f"{round(TSys[int(i/2)],2)} K")
            if i in indices:
                self.bbc_labels[i].setFont(font_chosen)
            else:
                self.bbc_labels[i].setFont(font_not_chosen)
            
            if TSys[int(i/2)] > 990:
                self.bbc_labels[i].setStyleSheet("background-color: red")
            else:
                self.bbc_labels[i].setStyleSheet("background-color: transparent")

class newScanStackingFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setUpNewFigure()
        self.__makeCrossHair()
        self.vlineTabTop = []
        self.vlineTabZoom = []
        self.pTop.setMouseEnabled(x=False, y=False)
        self.pZoom.setMouseEnabled(x=False, y=False)

    def mouseClicked(self, event):
        mp = self.pTop.vb.mapSceneToView(event.scenePos())
        print(f"Clicked: {mp.x()}")

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
        cyan = (255,255,255)
        red = (255, 127, 80)
        # --
        self.fullYScanPlot = self.pTop.plot([0,1], pen=cyan)
        self.zoomedYScanPlot = self.pZoom.plot([0,1], pen=cyan)
        self.fitChebyPlot = self.pZoom.plot([0,1], pen=pg.mkPen(red, width=2))
        # --
        self.pTop.disableAutoRange()
        self.pZoom.disableAutoRange()
        self.pTop.autoRange(0.0)
        self.pZoom.autoRange(0.0)
        # --
        self.pTop.scene().setMoveDistance(100)
        self.pZoom.scene().setMoveDistance(100)
        # --
        cursor = QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.pTop.setCursor(cursor)
        self.pZoom.setCursor(cursor)

    def __makeCrossHair(self):
        penw=pg.mkPen(color=(128,128,128), width=2 )
        self.xTopCross = pg.InfiniteLine(pos=0.0, angle=90.0, pen=penw)
        self.xZoomCross = pg.InfiniteLine(pos=0.0, angle=90.0, pen=penw)
        self.pTop.addItem(self.xTopCross)
        self.pZoom.addItem(self.xZoomCross)
        self.pTop.scene().sigMouseMoved.connect(self.__mouseMovedEvent)


    def __mouseMovedEvent(self, event):
        mp = self.pTop.vb.mapSceneToView(event)
        x = mp.x()
        self.xTopCross.setValue(x)
        self.xZoomCross.setValue(x)

    def drawVline(self, pos, wcolor):
        penw = pg.mkPen(color=wcolor, width=3, style=QtCore.Qt.DashLine)
        self.vlineTabTop.append(pg.InfiniteLine(pos=pos, angle=90.0, pen=penw))
        self.vlineTabZoom.append(pg.InfiniteLine(pos=pos, angle=90.0, pen=penw))
        self.pTop.addItem(self.vlineTabTop[len(self.vlineTabTop)-1] )
        self.pZoom.addItem(self.vlineTabZoom[len(self.vlineTabZoom)-1] )

    def clearVlines(self):
        [self.pTop.removeItem(i) for i in self.vlineTabTop]
        [self.pZoom.removeItem(i) for i in self.vlineTabZoom]
        vlineTabTop = []
        vlineTabZoom = []

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
        self.pZoom.setXRange(x.min(), x.max(), padding=0.0)
    
    def drawData(self):
        self.__autoscaleZoomedPlotY()
        self.autoscale()
    
    def autoscale(self):
        x,y = self.fullYScanPlot.getData()
        diff = abs(y.max() - y.min())
        maxRange = y.max() + 0.05 * diff
        minRange = y.min() - 0.05 * diff
        self.pTop.setYRange(minRange, maxRange, padding=0.0)

class stackedSpectrumFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__()
        self.__setUpNewFigure()
        self.p.setMouseEnabled(x=False, y=False)

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
        self.p.scene().setMoveDistance(100)
        # -
        cursor = QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.p.setCursor(cursor)

class otherPropsFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__()
        self.__setUpNewFigure()
        self.pTSys.setMouseEnabled(x=False, y=False)
        self.pTotal.setMouseEnabled(x=False, y=False)
        self.totalFluxPoints = []
        self.__makeHorizontalCrossHair()

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
        self.tsysPlot = self.pTSys.plot([0], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        self.actualTsysPlot = self.pTSys.plot([0], symbol='o', symbolSize=6, symbolBrush=lime, pen=None)
        #self.totalFluxPlot = self.pTotal.plot([0,1], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        # dots
        self.dot1Tsys = self.pTSys.plot( [0], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        self.dot2Tsys = self.pTSys.plot( [0], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        self.dotTF = self.pTotal.plot([0], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        # lines

        self.tsysVline = pg.InfiniteLine(pos=0.0, angle=90.0, pen=magenta)
        self.totalFluxVline = pg.InfiniteLine(pos=0.0, angle=90.0, pen=magenta)

        self.pTSys.addItem(self.tsysVline)
        self.pTotal.addItem(self.totalFluxVline)
        self.dotTF.setZValue(50)
        
        self.pTSys.setLabel(axis='left', text="Tsys (K)")
        self.pTotal.setLabel(axis='left', text="Total flux")
        self.pTotal.setLabel(axis='bottom', text="Hours since start")
        # --
        self.pTotal.scene().setMoveDistance(100)
        self.pTSys.scene().setMoveDistance(100)
        # --
        cursor = QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.pTotal.setCursor(cursor)
        self.pTSys.setCursor(cursor)

    
    def appendToTotalFluxPool(self, x ,y):
        blue=(100, 100, 255)
        eee = pg.ScatterPlotItem([x], [y], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        eee.setBrush(blue)
        self.pTotal.addItem(eee)
        self.totalFluxPoints.append(eee)
    
    def setTotalFluxStacked(self, index):
        if index >= len(self.totalFluxPoints):
            return
        limePen = (0,255,0)
        self.totalFluxPoints[index].setBrush(limePen)
    
    def setTotalFluxDiscarded(self, index):
        if index >= len(self.totalFluxPoints):
            return
        redPen = (192, 10, 10)
        self.totalFluxPoints[index].setBrush(redPen)
    
    def setDataForIndex(self, index, x, y):
        self.totalFluxPoints[index].setData([x],[y])

    def setTotalFluxDefaultBrush(self):
        blue=(100, 100, 255)
        [point.setBrush(blue) for point in self.totalFluxPoints]
    
    def __makeHorizontalCrossHair(self):
        blue=(100, 100, 255)
        penw = pg.mkPen(color=blue, width=2)
        self.yTFCross = pg.InfiniteLine(pos=0.0, angle=0.0, pen=penw)
        #self.xZoomCross = pg.InfiniteLine(pos=0.0, angle=90.0, pen=blue)
        self.pTotal.addItem(self.yTFCross)
        self.pTotal.scene().sigMouseMoved.connect(self.__mouseMovedEventTF)
    
    def __mouseMovedEventTF(self, event):
        mp = self.pTotal.vb.mapSceneToView(event)
        y = mp.y()
        self.yTFCross.setValue(y)
    
    def colorizePoints(self, threshold):
        for i in range(len(self.totalFluxPoints)):
            x,y = self.totalFluxPoints[i].getData()
            if y.max() > threshold:
                self.setTotalFluxDiscarded(i)
            else:
                self.setTotalFluxStacked(i)