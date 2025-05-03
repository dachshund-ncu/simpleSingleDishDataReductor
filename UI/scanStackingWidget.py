"""
Class, that holds the scan stacking widget:
-> plotting actual scans
-> plotting stacked spectrum
-> plotting z(t), tsys(t), total flux(t)
-> labels: scans, tsys, rms, snr, peak
"""

#from tkinter import Y
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction

from .icons import rectangle_xmark_icon
from .ui_elements.customLeftBarWidget import cWidget
from .ui_elements.custom_widget import custom_widget, CustomWidgetSemiTransparent
from .ui_elements.customButton import custom_button
from .ui_elements.custom_label import custom_label
from .ui_elements.horizontal_separator import CustomHorizontalSeparator
from .ui_elements.custom_menu import CustomMenu
from .ui_elements.custom_toolbar import CustomToolbar
from .scanStackerElements import newScanStackingFigure, stackedSpectrumFigure, otherPropsFigure
from .icons import *
import pyqtgraph as pg

class scanStackingWidget(custom_widget):
    def __init__(self, parent=None):
        """
        initializing the widget:
        -> will initialize the layout
        -> will declare necessary widgets and place them correctly
        """
        custom_widget.__init__(self)
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.newScanFigure = newScanStackingFigure()
        self.newStackedFigure = stackedSpectrumFigure()
        self.newOtherPropsFigure = otherPropsFigure()
        self.__declareNecessaryButtons()
        self.__addIconsToButtons()
        self.__wrapFiguresInWidgets()
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
        self.scanTbar = CustomToolbar()
        self.leftWidget = cWidget()
        self.vboxLeftWidget = QtWidgets.QVBoxLayout(self.leftWidget )
        self.vboxLeftWidget.setContentsMargins(0,0,0,0)
        self.nextPrevScanLayout = QtWidgets.QHBoxLayout()
        # buttons
        self.addToStack = custom_button("  Add to stack")
        self.discardFromStack = custom_button("  Discard from stack")
        self.removeFromStack = custom_button("  Remove from stack")
        self.removeChannels = custom_button("  Remove channels")
        self.performRemoval = custom_button("  Perform Removal")
        self.cancelRemoval = custom_button("  Cancel Removal")
        self.performPolyFit = custom_button("  Perform Polyfit")
        self.fitPolynomial = custom_button("  Fit polynomial mode")
        self.automaticReduction = custom_button("  Automatic mode")
        self.nextScan = QAction("")
        self.prevScan = QAction("")
        self.openMenu = QAction("")
        self.finishPol = custom_button("  Finish LHC")
        # labels
        # -- scan properties --
        self.grid_labels = QtWidgets.QGridLayout()
        self.props_labels = [custom_label("label {i}") for i in range(10)]
        # -- BBC --
        self.bbc_labels = [custom_label(f"label {i}") for i in range(8)]

        # labels placing
        for i in range(len(self.props_labels)):
            self.grid_labels.addWidget(self.props_labels[i], int(i/2), int(i%2))

        for i in range(len(self.bbc_labels)):
            self.grid_labels.addWidget(self.bbc_labels[i], int(i/2) + 5, int(i%2))

        # buttons placing
        def spacer():
            s = QtWidgets.QWidget()
            s.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                            QtWidgets.QSizePolicy.Preferred)
            return s
        self.scanTbar.addAction(self.prevScan)
        self.scanTbar.addWidget(spacer())
        self.scanTbar.addAction(self.openMenu)
        self.scanTbar.addWidget(spacer())
        self.scanTbar.addAction(self.nextScan)

        self.vboxLeftWidget.addWidget(self.scanTbar)
        self.vboxLeftWidget.addWidget(self.addToStack)
        self.vboxLeftWidget.addWidget(self.discardFromStack)
        self.vboxLeftWidget.addWidget(self.removeFromStack)
        self.vboxLeftWidget.addSpacing(8)
        self.vboxLeftWidget.addWidget(CustomHorizontalSeparator())
        self.vboxLeftWidget.addSpacing(8)
        self.vboxLeftWidget.addWidget(self.removeChannels)
        self.vboxLeftWidget.addWidget(self.fitPolynomial)
        self.vboxLeftWidget.addWidget(self.automaticReduction)
        self.vboxLeftWidget.addSpacing(8)
        self.vboxLeftWidget.addWidget(CustomHorizontalSeparator())
        self.vboxLeftWidget.addSpacing(8)
        self.vboxLeftWidget.addWidget(self.performPolyFit)
        self.vboxLeftWidget.addWidget(self.performRemoval)
        self.vboxLeftWidget.addWidget(self.cancelRemoval)
        self.vboxLeftWidget.addWidget(self.finishPol)
        self.vboxLeftWidget.addStretch()

    def __addIconsToButtons(self):
        self.addToStack.setIcon(confirmation_icon)
        self.discardFromStack.setIcon(x_mark_icon)
        self.nextScan.setIcon(arrow_right_icon)
        self.prevScan.setIcon(arrow_left_icon)
        self.removeFromStack.setIcon(trash_can_icon)
        self.fitPolynomial.setIcon(chart_line_icon)
        self.removeChannels.setIcon(eraser_icon)
        self.automaticReduction.setIcon(robot_icon)
        self.performRemoval.setIcon(minus_solid_icon)
        self.cancelRemoval.setIcon(ban_icon)
        self.performPolyFit.setIcon(play_icon)
        self.finishPol.setIcon(flag_icon)
        self.openMenu.setIcon(bars_icon)


    def __placeNecessaryButtons(self):
        # layouts placing
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.leftWidget, 0, 0, 3, 1)
        self.layout.addWidget(self.newScanFigureWidget, 0, 1, 2,1)
        self.layout.addWidget(self.newStackedFigureWidget, 2, 1, 1, 1)
        self.layout.addWidget(self.newOtherPropsFigureWidget, 0, 2, 2, 1)
        self.layout.addWidget(self.labelsWidget, 2,2, 1,1)

        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,3)
        self.layout.setColumnStretch(2,2)
        [self.layout.setRowStretch(i, 1) for i in range(self.layout.rowCount())]

    def __defaultSettings(self):
        self.fitPolynomial.setCheckable(True)
        self.removeChannels.setCheckable(True)
        self.automaticReduction.setCheckable(True)
        self.fitPolynomial.setChecked(True)

    def __wrapFiguresInWidgets(self):
        """
        Simply wraps transparent figures in custom widgets
        """
        self.newScanFigureWidget = CustomWidgetSemiTransparent()
        layoutNSFW = QtWidgets.QVBoxLayout(self.newScanFigureWidget)
        layoutNSFW.setContentsMargins(0,0,0,0)
        layoutNSFW.addWidget(self.newScanFigure)
        self.newStackedFigureWidget = CustomWidgetSemiTransparent()
        layoutNSFW = QtWidgets.QVBoxLayout(self.newStackedFigureWidget)
        layoutNSFW.setContentsMargins(0, 0, 0, 0)
        layoutNSFW.addWidget(self.newStackedFigure)
        self.newOtherPropsFigureWidget = CustomWidgetSemiTransparent()
        layoutNSFW = QtWidgets.QVBoxLayout(self.newOtherPropsFigureWidget)
        layoutNSFW.setContentsMargins(0, 0, 0, 0)
        layoutNSFW.addWidget(self.newOtherPropsFigure)
        # ----------
        self.labelsWidget = CustomWidgetSemiTransparent()
        self.labelsWidget.setLayout(self.grid_labels)


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
        """
        Simple sets label accordong to scan properties
        TODO: refactoring needed!!!
        """

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
                self.bbc_labels[i].setBackgroundColor("red")
            else:
                self.bbc_labels[i].setBackgroundColor("transparent")

