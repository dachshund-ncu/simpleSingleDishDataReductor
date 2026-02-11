from .moreEfficentFigureTemplate import templateFigurePG
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5 import QtCore
import numpy as np

class newScanStackingFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setUpNewFigure()
        self.__makeCrossHair()
        self.vlineTabTop = []
        self.vlineTabZoom = []
        self.pTop.setMouseEnabled(x=False, y=False)
        self.pZoom.setMouseEnabled(x=False, y=False)
        self.setBackground(None)

    def mouseClicked(self, event):
        mp = self.pTop.vb.mapSceneToView(event.scenePos())
        print(f"Clicked: {mp.x()}")

    def __setUpNewFigure(self):
        # self.newScanFigure()
        self.pTop = self.addPlot(name='TopPlot')
        self.nextRow()
        self.pZoom = self.addPlot(name='ZoomPlot')
        self.pTop.setXLink(self.pZoom)
        # -
        self.pTop.showGrid(x=True, y=True, alpha=0.2)
        self.pZoom.showGrid(x=True, y=True, alpha=0.2)
        # PENS
        cyan = (255, 255, 255)
        red2 = (255, 127, 80)
        grey = (137, 137, 137)
        green = (191, 255, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        # --

        self.fullYScanPlots = {
            "continuum": self.pTop.plot([0, 1], pen=grey),
            "emission": self.pTop.plot([0, 1], pen=green),
            "rfi": self.pTop.plot([0, 1], pen=red2),
            "edge": self.pTop.plot([0, 1], pen=blue)
        }

        self.zoomedYScanPlots = {
            "continuum": self.pZoom.plot([0, 1], pen=grey),
            "emission": self.pZoom.plot([0, 1], pen=green),
            "rfi": self.pZoom.plot([0, 1], pen=red2),
            "edge": self.pZoom.plot([0, 1], pen=blue)
        }

        self.fitChebyPlot = self.pZoom.plot([0, 1], pen=pg.mkPen(red, width=2))
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
        penw = pg.mkPen(color=(128, 128, 128), width=2)
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
        self.pTop.addItem(self.vlineTabTop[len(self.vlineTabTop) - 1])
        self.pZoom.addItem(self.vlineTabZoom[len(self.vlineTabZoom) - 1])

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
        x, y = self.fitChebyPlot.getData()
        max = y.max()
        min = y.min()
        diff = max - min
        lowerEnd = min - 2.0 * diff
        upperEnd = max + 2.0 * diff
        self.pZoom.setYRange(lowerEnd, upperEnd)
        self.pZoom.setXRange(x.min(), x.max(), padding=0.0)

    def drawData(self):
        self.__autoscaleZoomedPlotY()
        self.autoscale()

    def gather_data_from_plot_d(self):
        # gather data from all plots
        x = []
        y = []
        for key in self.fullYScanPlots.keys():
            tmp_x, tmp_y = self.fullYScanPlots[key].getData()
            x.extend(tmp_x)
            y.extend(tmp_y)
        x = np.asarray(x)
        y = np.asarray(y)
        # replace nans with 9
        x[np.isnan(x)] = 0.0
        y[np.isnan(y)] = 0.0
        return x, y

    def autoscale(self):
        x, y = self.gather_data_from_plot_d()
        diff = abs(y.max() - y.min())
        maxRange = y.max() + 0.05 * diff
        minRange = y.min() - 0.05 * diff
        self.pTop.setYRange(minRange, maxRange, padding=0.0)


class stackedSpectrumFigure(templateFigurePG):
    def __init__(self, parent=None):
        super().__init__()
        self.__setUpNewFigure()
        self.p.setMouseEnabled(x=False, y=False)
        self.setBackground(None)

    def __setUpNewFigure(self):
        # self.newScanFigure()
        self.p = self.addPlot(name='Stacked Plot')
        # --
        self.p.showGrid(x=True, y=True, alpha=0.2)
        # --
        orange = (255, 165, 0)
        silver = (128, 128, 128)
        self.spectrumToStackPlot = self.p.plot([0, 1], pen=silver)
        self.stackPlot = self.p.plot([0, 1], pen=orange)
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
        self.setBackground(None)

    def __setUpNewFigure(self):
        self.pTSys = self.addPlot(name='tsysPlot')
        self.nextRow()
        self.pTotal = self.addPlot(name='totalPlot')
        self.pTSys.setXLink(self.pTotal)
        # -
        self.pTSys.showGrid(x=True, y=True, alpha=0.2)
        self.pTotal.showGrid(x=True, y=True, alpha=0.2)
        # ---
        # ---
        blue = (100, 100, 255)
        lime = (0, 255, 0)
        magenta = (255, 0, 255)
        self.tsysPlot = self.pTSys.plot([0], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        self.actualTsysPlot = self.pTSys.plot([0], symbol='o', symbolSize=6, symbolBrush=lime, pen=None)
        # self.totalFluxPlot = self.pTotal.plot([0,1], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        # dots
        self.dot1Tsys = self.pTSys.plot([0], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
        self.dot2Tsys = self.pTSys.plot([0], symbol='o', symbolSize=7, symbolBrush=magenta, pen=None)
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

    def appendToTotalFluxPool(self, x, y):
        blue = (100, 100, 255)
        eee = pg.ScatterPlotItem([x], [y], symbol='o', symbolSize=6, symbolBrush=blue, pen=None)
        eee.setBrush(blue)
        self.pTotal.addItem(eee)
        self.totalFluxPoints.append(eee)

    def setTotalFluxStacked(self, index):
        if index >= len(self.totalFluxPoints):
            return
        limePen = (0, 255, 0)
        self.totalFluxPoints[index].setBrush(limePen)

    def setTotalFluxDiscarded(self, index):
        if index >= len(self.totalFluxPoints):
            return
        redPen = (192, 10, 10)
        self.totalFluxPoints[index].setBrush(redPen)

    def setDataForIndex(self, index, x, y):
        self.totalFluxPoints[index].setData([x], [y])

    def setTotalFluxDefaultBrush(self):
        blue = (100, 100, 255)
        [point.setBrush(blue) for point in self.totalFluxPoints]

    def __makeHorizontalCrossHair(self):
        blue = (100, 100, 255)
        penw = pg.mkPen(color=blue, width=2)
        self.yTFCross = pg.InfiniteLine(pos=0.0, angle=0.0, pen=penw)
        # self.xZoomCross = pg.InfiniteLine(pos=0.0, angle=90.0, pen=blue)
        self.pTotal.addItem(self.yTFCross)
        self.pTotal.scene().sigMouseMoved.connect(self.__mouseMovedEventTF)

    def __mouseMovedEventTF(self, event):
        mp = self.pTotal.vb.mapSceneToView(event)
        y = mp.y()
        self.yTFCross.setValue(y)

    def colorizePoints(self, threshold):
        for i in range(len(self.totalFluxPoints)):
            x, y = self.totalFluxPoints[i].getData()
            if y.max() > threshold:
                self.setTotalFluxDiscarded(i)
            else:
                self.setTotalFluxStacked(i)