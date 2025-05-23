'''
Class, that holds the Main Window of the program
Author: Michał Durjasz
Date: 8.03.2022
'''
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QRect

from .scanStackingWidget import scanStackingWidget
from .polEndWidget import polEndWidget
from .finishWidget import finishWidgetP
from .fitOrderChangeWidget import changeOrder
from .manualCalCoeffSetter import changeCalCoeffWindow
from .ui_elements.custom_menu import CustomMenu
from .icons import bars_icon
import numpy as np
import sys
import functools as fctls

# -- class definition starts here --
class mainWindowWidget(QtWidgets.QMainWindow):
    # -- init --
    def __init__(
            self,
            data = None,
            calibrate=True):
        super().__init__()
        self.setVisible(False)
        '''
        This is an initialising method. In it, we will place buttons
        and other widgets correctly, by using private methods below:
        Also we will initialize data reduction by plotting data, if we can:
        '''
        self.calibrate = calibrate
        self.calibrated = False
        self.BBCs = [1,2]
        self.bbcindex = 0
        self.__declareAndPlaceButtons()

        self.lhcReduction = True
        self.mode = 'Polynomial fit'
        if data != None:
            self.data = data
            self.actualScanNumber = 0
            self.actualBBC = self.BBCs[0]
            self.maximumScanNumber = len(data.obs.mergedScans)
            self.timeInfoAlreadyPlotted = False
        self.__declareMenu()
        self.__declareAndPlaceCustomWidgets()
        if data != None:
            self.__plotTimeInfo()
            self.__plotScanNo(self.actualScanNumber)

        self.__setCheckedBBCActions()
        self.__connectButtonsToSlots()
        self.__setPolyFitMode()
        self.setStyleSheet("background-color: #121212;")
        self.setVisible(True)
        if self.data is not None and len(self.data.caltabs) < 1:
            self.display_caltab_prompt("Seems there are no downloaded caltabs. Would you like to download them?")
        

    def __declareAndPlaceButtons(self):
        '''
        This methood will declare and place buttons correctly. There
        is also declared layout (QGrid) and primary widget(window), so watch out for that.
        Maybe it would be better to declare it separately?
        Buttons will be placed in the groupBoxes
        '''
        # layouts
        self.window = QtWidgets.QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QtWidgets.QGridLayout(self.window)
        # shortcuts
        self.firstOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('1'), self)
        self.secondOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('2'), self)
        self.thirdOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('3'), self)
        self.fourthOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('4'), self)
        self.fifthtOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('5'), self)
        self.sixthOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('6'), self)
        self.seventhOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('7'), self)
        self.eighthOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('8'), self)
        self.ninthOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('9'), self)
        self.tenthOrderFit = QtWidgets.QShortcut(QtGui.QKeySequence('t'), self)

        self.shrtAddToStack = QtWidgets.QShortcut(QtGui.QKeySequence('k'), self)
        self.shrtDiscardToStack = QtWidgets.QShortcut(QtGui.QKeySequence('d'), self)
        self.shrtNextScan = QtWidgets.QShortcut(QtGui.QKeySequence('right'), self)
        self.shrtPrevScan = QtWidgets.QShortcut(QtGui.QKeySequence('left'), self)
        self.shrtNextPol = QtWidgets.QShortcut(QtGui.QKeySequence('n'), self)
        self.shrtEndRed = QtWidgets.QShortcut(QtGui.QKeySequence('p'), self)
        self.shrtremoveChansMode = QtWidgets.QShortcut(QtGui.QKeySequence('r'), self)
        self.shrtfitPolyMode = QtWidgets.QShortcut(QtGui.QKeySequence('f'), self)
        self.shrtAutoRedMode = QtWidgets.QShortcut(QtGui.QKeySequence('i'), self)
        self.setDefaultRangeOnPolEndShrt = QtWidgets.QShortcut(QtGui.QKeySequence('b'), self)

    def __declareAndPlaceCustomWidgets(self):
        """
        Declares custom widgets, defined in separate files
        Only self.scanStacker should be visible at the start of the program
        """
        self.scanStacker = scanStackingWidget()
        self.polEnd = polEndWidget()
        self.finishW = finishWidgetP()
        self.orderChanger = changeOrder()
        self.calCoeffChanger = changeCalCoeffWindow()
        self.layout.addWidget(self.scanStacker, 0, 1, 2, 1)
    
    def __declareMenu(self):
        """
        This method solely declares and places menu in the top of the Main Window
        """
        #--
        self.menu = CustomMenu()
        self.menu.setToolTip("Advanced")
        self.menu.setStyleSheet(CustomMenu.get_style_sheet())

        # --
        self.changeOrderAction = QtWidgets.QAction("Change fit order")
        # --
        self.menu.addAction(self.changeOrderAction)
        self.changeBbcLhc = self.menu.addMenu("BBC for LHC")
        self.changeBbcRhc = self.menu.addMenu("BBC for RHC")
        self.changeBBCLHCActions = []
        self.changeBBCRHCActions = []
        for i in range(len(self.data.obs.mergedScans[0].pols)):
            self.changeBBCLHCActions.append(QtWidgets.QAction("BBC " + str(i+1)))
            self.changeBBCRHCActions.append(QtWidgets.QAction("BBC " + str(i+1)))
            self.changeBBCLHCActions[i].setCheckable(True)
            self.changeBBCRHCActions[i].setCheckable(True)
        for i in self.changeBBCLHCActions:
            self.changeBbcLhc.addAction(i)
        for i in self.changeBBCRHCActions:
            self.changeBbcRhc.addAction(i)
        # -- caltab loading
        self.download_caltabs_a = QtWidgets.QAction("Download caltabs")
        self.menu.addAction(self.download_caltabs_a)

    def showMenu(self):
        action_widget = self.scanStacker.scanTbar.widgetForAction(self.scanStacker.openMenu)
        if action_widget:
            rect = action_widget.rect()
            center_bottom = rect.center()
            center_bottom.setY(rect.bottom())
            point = action_widget.mapToGlobal(center_bottom)
            self.menu.exec_(point)

    def __setCheckedBBCActions(self):
        """
        This method sets checked actions for BBCs
        We want only the 1 BBC per pol to be checked
        We manage that by executing the code below
        self.BBCs is the list of used BBCs: by default these are [1,2]
        """
        self.changeBBCLHCActions[self.BBCs[0]-1].setChecked(True)
        self.changeBBCRHCActions[self.BBCs[1]-1].setChecked(True)
        

    def __connectButtonsToSlots(self):
        """
        This method connects buttons and actions to the corresponding slots
        """
        # -- scan stacker --
        self.scanStacker.nextScan.triggered.connect(self.__nextScanSlot)
        self.scanStacker.prevScan.triggered.connect(self.__prevScanSlot)
        self.scanStacker.openMenu.triggered.connect(self.showMenu)
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
        # -- pol end widget --
        self.polEnd.backToPol.clicked.connect(self.__returnToScanEdit)
        self.polEnd.goToNextPol.clicked.connect(self.__goToNextPol)
        self.polEnd.performFit.clicked.connect(self.__fitToFinalSpectum)
        self.polEnd.performRemoval.clicked.connect(self.__removeOnFinalSpectrum)
        self.polEnd.reverseChanges.clicked.connect(self.__cancelChangesOnFinalSpectrum)
        self.polEnd.cancelCalibrations.clicked.connect(self.__uncalibrateData)
        self.polEnd.useCalibrations.clicked.connect(self.__calibrateData)
        self.polEnd.setManualCal.clicked.connect(self.__showManualCalCoeffWidget)
        self.polEnd.setDefaultRangeButton.clicked.connect(self.__setAutoRangeOnPolEndPlot)
        self.calCoeffChanger.apply.clicked.connect(self.__setCalCoeffManually)
        # -- both stacker and end widget --
        self.changeOrderAction.triggered.connect(self.__showFitOrderWidget)
        self.orderChanger.cancel.clicked.connect(self.__cancelFitOrderChange)
        self.orderChanger.apply.clicked.connect(self.__changeFitOrder)
        # -- finish widget --
        self.finishW.endDataReduction.clicked.connect(self.__closeApp)
        # -- fit shortcuts --
        self.firstOrderFit.activated.connect(self.__setFirstOrderPoly)
        self.secondOrderFit.activated.connect(self.__setsecondOrderPoly)
        self.thirdOrderFit.activated.connect(self.__setThirdOrderPoly)
        self.fourthOrderFit.activated.connect(self.__setFourthOrderPoly)
        self.fifthtOrderFit.activated.connect(self.__setFifthOrderPoly)
        self.sixthOrderFit.activated.connect(self.__setSixthOrderPoly)
        self.seventhOrderFit.activated.connect(self.__setSeventhOrderPoly)
        self.eighthOrderFit.activated.connect(self.__setEightOrderPoly)
        self.ninthOrderFit.activated.connect(self.__setNinthOrderPoly)
        self.tenthOrderFit.activated.connect(self.__setTenthOrderPoly)
        # -- THIS (or in more phythonic language: self) --
        self.shrtAddToStack.activated.connect(self.__addToStackSlot)
        self.shrtDiscardToStack.activated.connect(self.__discardScan)
        self.shrtNextScan.activated.connect(self.__nextScanSlot)
        self.shrtPrevScan.activated.connect(self.__prevScanSlot)
        self.shrtNextPol.activated.connect(self.__goToNextPol)
        self.shrtEndRed.activated.connect(self.__closeApp)
        self.shrtremoveChansMode.activated.connect(self.__shrtRemWrapper)
        self.shrtfitPolyMode.activated.connect(self.__shrtPolyWrapper)
        self.shrtAutoRedMode.activated.connect(self.__shrtAutoWrapper)
        self.setDefaultRangeOnPolEndShrt.activated.connect(self.__setAutoRangeOnPolEndPlot)
        self.download_caltabs_a.triggered.connect(self.download_caltabs)
        # --- Menu  - selecting BBCs ---
        for i in range(len(self.changeBBCLHCActions)):
            self.changeBBCLHCActions[i].triggered.connect(fctls.partial(self.__bbcLhcHandler, i))
        for i in range(len(self.changeBBCRHCActions)):
            self.changeBBCRHCActions[i].triggered.connect(fctls.partial(self.__bbcRhcHandler, i))

    def plot_spectral_data(
            self,
            plot_dictionary,
            categories: np.ndarray,
            x_data: np.ndarray,
            y_data: np.ndarray):
        category_d = {
            "continuum": 0,
            "rfi": 1,
            "emission": 2,
            "edge": 3
        }
        # set data for keys
        y_data_dict = {}
        for key in plot_dictionary.keys():
            tmp_y = y_data.copy()
            tmp_y[categories != category_d[key]] = np.nan
            y_data_dict[key] = tmp_y
        # plot data
        for key in plot_dictionary.keys():
            plot_dictionary[key].setData(
                x_data,
                y_data_dict[key]
            )

    def __getCategoriesFromBounds(
            self,
            bounds: list[list[int]],
            x_data: np.ndarray):
        category_d = {
            "continuum": 0,
            "rfi": 1,
            "emission": 2,
            "edge": 3
        }
        # get list of categories
        categories = np.full(len(x_data), category_d["rfi"])
        for channel_pair in bounds:
            if channel_pair[0] < 0: channel_pair[0] = 0
            if channel_pair[1] > x_data[-1]: channel_pair[1] = int(x_data[-1])
            categories[channel_pair[0]:channel_pair[1]] = category_d["continuum"]
        return categories

    def __plotScanNo(self, scanNumber):
        """
        It plots scan of the number, given in the argument
        WHAT IT DOES:
        -> fits the polynomial (right before plottng)
        -> puts on the graphs:
        --> merged scan
        --> zoomed merged scan + poly fit
        --> resulting spectrum
        -> also marks, which Z, Tsys and Total Flux we are at
        """
        if self.lhcReduction:
            self.actualBBC = self.BBCs[0]
            self.data.setActualBBC(self.actualBBC)
        else:
            self.actualBBC = self.BBCs[1]
            self.data.setActualBBC(self.actualBBC)
        # ------------
        if scanNumber > len(self.data.obs.mergedScans):
            return
        # ------------

        # ------------
        if len(self.scanStacker.fitBoundsChannels) != 0:
            self.data.fitBoundsChannels = self.scanStacker.fitBoundsChannels
        # ------------

        noOfChannels = len(self.data.obs.mergedScans[scanNumber].pols[0])
        channelTab = np.linspace(1, noOfChannels, noOfChannels)
        # self.scanStacker.newScanFigure.fullYScanPlot.setData(channelTab, self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1])
        # self.scanStacker.newScanFigure.zoomedYScanPlots["continuum"].setData(channelTab, self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1])
        self.plot_spectral_data(
            plot_dictionary = self.scanStacker.newScanFigure.fullYScanPlots,
            categories = self.__getCategoriesFromBounds(self.data.fitBoundsChannels, channelTab),
            x_data = channelTab,
            y_data = self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1]
        )
        self.plot_spectral_data(
            plot_dictionary = self.scanStacker.newScanFigure.zoomedYScanPlots,
            categories = self.__getCategoriesFromBounds(self.data.fitBoundsChannels, channelTab),
            x_data = channelTab,
            y_data = self.data.obs.mergedScans[scanNumber].pols[self.actualBBC-1]
        )
        # ------------

        #print(self.data.fitBoundsChannels)
        polyTabX, polyTabY, polyTabResiduals = self.data.fitChebyForScan(self.actualBBC, self.data.fitOrder, scanNumber)
        self.scanStacker.newScanFigure.fitChebyPlot.setData(polyTabX, polyTabY)
        self.scanStacker.setFitDone()
        self.scanStacker.newStackedFigure.spectrumToStackPlot.setData(range(len(polyTabResiduals)), polyTabResiduals)

        
        self.scanStacker.setVline(self.data.mergedTimeTab[self.actualScanNumber])
        # --
        stackPlot = self.data.calculateSpectrumFromStack()
        if len(stackPlot) == 1:
            self.scanStacker.finishPol.setEnabled(False)
            self.scanStacker.newStackedFigure.stackPlot.setData([])
        else:
            self.scanStacker.finishPol.setEnabled(True)
            self.scanStacker.newStackedFigure.stackPlot.setData(range(len(stackPlot)), stackPlot)
        # --
        timesDot = [self.data.timeTab[2* self.actualScanNumber], self.data.timeTab[2 * self.actualScanNumber+1]]
        tsysDot = [self.data.tsysTab[self.actualBBC-1][2 * self.actualScanNumber], self.data.tsysTab[self.actualBBC-1][2 * self.actualScanNumber + 1] ]
        totalFluxDot = self.data.totalFluxTab[self.actualBBC-1][self.actualScanNumber]
        zDot = [self.data.zTab[2 * self.actualScanNumber], self.data.zTab[2 * self.actualScanNumber+1] ]
        self.scanStacker.setDots(timesDot, tsysDot, zDot, totalFluxDot )
        self.scanStacker.updateDataPlots()
        self.__updateLabel()


    
    def __plotTimeInfo(self):
        '''
        It plots info about Tsys vs time and total flux vs time
        It is meant to be called only once per pol
        '''
        tmptsys = []
        tmptime = []
        for i in self.data.tsysTab:
            tmptsys.extend(i)
            tmptime.extend(self.data.timeTab)
            
        self.scanStacker.newOtherPropsFigure.tsysPlot.setData(tmptime, tmptsys)
        self.scanStacker.newOtherPropsFigure.actualTsysPlot.setData(self.data.timeTab, self.data.tsysTab[self.actualBBC-1])
        
        for i in range(len(self.data.totalFluxTab[self.actualBBC-1])):
            if not self.timeInfoAlreadyPlotted:
                self.scanStacker.newOtherPropsFigure.appendToTotalFluxPool(self.data.mergedTimeTab[i], self.data.totalFluxTab[self.actualBBC-1][i])
            else:
                self.scanStacker.newOtherPropsFigure.setDataForIndex(i, self.data.mergedTimeTab[i], self.data.totalFluxTab[self.actualBBC-1][i])
        self.timeInfoAlreadyPlotted = True

    def display_caltab_prompt(self, text: str) -> None:
        '''
        Displays caltab propt if there is no caltab loaded
        '''
        msgBox = QtWidgets.QMessageBox()
        downloadBtn = msgBox.addButton("Download caltabs", QtWidgets.QMessageBox.ActionRole)
        cancelBtn = msgBox.addButton(QtWidgets.QMessageBox.Abort)
        msgBox.setText(text)
        msgBox.exec()
        if msgBox.clickedButton() == downloadBtn:
            self.download_caltabs()
        elif msgBox.clickedButton() == cancelBtn:
            return
    
    def __display_download_caltabs_propmpt(self, isSuccess: bool):
        '''
        Meant to be triggered only after the caltabs are downloaded
        Use with caution
        '''

        msgBox = QtWidgets.QMessageBox()
        if isSuccess:
            text = "Downloaded caltabs:"
            for c in self.data.caltabs:
                text += f"\n{c.label}, MJD {c.getMinEpoch()} -->  {c.getMaxEpoch()}"
        else:
            text = "Failed to download caltabs. Check internet connection or \"caltabPaths.ini\""
        msgBox.setText(text)
        msgBox.exec()
    '''
    Methods below are being used as SLOTS
    '''
    @QtCore.pyqtSlot()
    def __nextScanSlot(self):
        if self.actualScanNumber+1 < self.maximumScanNumber:
            self.actualScanNumber += 1
        else:
            self.actualScanNumber = 0
        
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __prevScanSlot(self):
        if self.actualScanNumber-1 >= 0:
            self.actualScanNumber -= 1
        else:
            self.actualScanNumber = self.maximumScanNumber-1
        
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __addToStackSlot(self):
        '''
        Adds to stack of reduced spectra
        'STACK' is being averaged, what gives better and better SNR with every addition
        UPDATE:
        if 'autoReductionMode' is activated, it will try to perform it with discarding standard adding to stack procedure
        if auto procedure fails for some reason, it will do standard task anyway
        '''
        if not self.scanStacker.isVisible():
            return
        if self.scanStacker.autoRedMode:
            flag = self.doAutoReduction()
            if flag:
                self.__finishPol()
                return
        self.data.addToStack(self.actualScanNumber)
        if self.data.checkIfAllScansProceeded():
            self.scanStacker.newOtherPropsFigure.setTotalFluxStacked(self.actualScanNumber)
            self.__plotScanNo(self.actualScanNumber)
            self.__finishPol()
        else:
            #print(f'Setting stacked {self.actualScanNumber}')
            self.scanStacker.newOtherPropsFigure.setTotalFluxStacked(self.actualScanNumber)
            self.__nextScanSlot()
            
    @QtCore.pyqtSlot()
    def __deleteFromStackSlot(self):
        self.data.deleteFromStack(self.actualScanNumber)
        self.scanStacker.newOtherPropsFigure.setTotalFluxDiscarded(self.actualScanNumber)
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __finishPol(self):
        # data
        
        # UI
        self.scanStacker.setVisible(False)
        self.layout.removeWidget(self.scanStacker)
        self.layout.addWidget(self.polEnd, 0, 1)
        self.polEnd.setVisible(True)

        if self.lhcReduction:
            self.changeBbcLhc.setEnabled(False)
        else:
            self.changeBbcRhc.setEnabled(False)

        # polyfitmode
        self.polEnd.setPolyFitMode()
        # data handling
        calCoeff = 1
        flag_cal = False
        if self.calibrate and self.data.properCaltabIndex < len(self.data.caltabs):
            date = self.data.obs.mjd
            flag_cal = self.data.findCalCoefficients()
            if self.lhcReduction:
                ctabx = self.data.caltabs[self.data.properCaltabIndex].lhcMJDTab
                ctaby = self.data.caltabs[self.data.properCaltabIndex].lhcCoeffsTab
                calCoeff = self.data.calCoeffLHC
            else:
                ctabx = self.data.caltabs[self.data.properCaltabIndex].rhcMJDTab
                ctaby = self.data.caltabs[self.data.properCaltabIndex].rhcCoeffsTab
                calCoeff = self.data.calCoeffRHC
            
            self.polEnd.plotCalCoeffsTable(ctabx, ctaby)
            self.polEnd.plotUsedCalCoeff(date, calCoeff)
            #self.data.printCalibrationMessage(calCoeff, date, self.lhcReduction)
            self.calibrated = True
            self.polEnd.cancelCalibrations.setEnabled(True)
            self.polEnd.useCalibrations.setEnabled(False)

        else:
            self.polEnd.cancelCalibrations.setEnabled(False)
            self.polEnd.useCalibrations.setEnabled(False)
        

        self.data.calculateSpectrumFromStack()
        spectr = self.data.calibrate(lhc=self.lhcReduction)
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], spectr)
        self.polEnd.setFluxLabel(calCoeff)
        if not flag_cal and self.calibrate:
            self.display_caltab_prompt(f"Seems that the calibration tables are too short. \nLast epoch in {self.data.caltabs[self.data.properCaltabIndex].label} is {self.data.caltabs[self.data.properCaltabIndex].getMaxEpoch()}, while epoch of this obs. is {round(self.data.obs.mjd,3)}.\nWould you like to download them?")
    @QtCore.pyqtSlot()
    def __discardScan(self):
        self.data.discardFromStack(self.actualScanNumber)
        self.scanStacker.newOtherPropsFigure.setTotalFluxDiscarded(self.actualScanNumber)
        if self.data.checkIfAllScansProceeded():
            self.__plotScanNo(self.actualScanNumber)
            self.__finishPol()
        else:
            self.__nextScanSlot()

    @QtCore.pyqtSlot()
    def __setPolyFitMode(self):
        self.scanStacker.polyFitMode = True
        self.scanStacker.removeChannelsMode = False
        self.scanStacker.autoRedMode = False
        self.scanStacker.fitPolynomial.setChecked(True)
        self.scanStacker.removeChannels.setChecked(False)
        self.scanStacker.automaticReduction.setChecked(False)
        self.scanStacker.performRemoval.setEnabled(False)
        self.scanStacker.cancelRemoval.setEnabled(False)
        self.scanStacker.performPolyFit.setEnabled(True)
        self.scanStacker.removeLines()
        self.scanStacker.newOtherPropsFigure.yTFCross.setVisible(False)
        self.mode = 'Polynomial fit'
        self.__updateLabel()
        print("-----> Polynomial fit mode is ACTIVE!")

    @QtCore.pyqtSlot()
    def __setRemoveChansMode(self):
        self.scanStacker.polyFitMode = False
        self.scanStacker.removeChannelsMode = True
        self.scanStacker.autoRedMode = False
        self.scanStacker.fitPolynomial.setChecked(False)
        self.scanStacker.removeChannels.setChecked(True)
        self.scanStacker.automaticReduction.setChecked(False)
        self.scanStacker.performRemoval.setEnabled(True)
        self.scanStacker.cancelRemoval.setEnabled(True)
        self.scanStacker.performPolyFit.setEnabled(False)
        self.scanStacker.setBoundChannels(self.data.fitBoundsChannels)
        self.scanStacker.resetRemoveChans()
        self.scanStacker.removeLines()
        self.scanStacker.newOtherPropsFigure.yTFCross.setVisible(False)
        self.mode = 'Remove channels'
        self.__updateLabel()
        print("-----> Channel removal mode is ACTIVE!")
    
    @QtCore.pyqtSlot()
    def __setAutoReductionMode(self):
        self.scanStacker.polyFitMode = False
        self.scanStacker.removeChannelsMode = False
        self.scanStacker.autoRedMode = True
        self.scanStacker.fitPolynomial.setChecked(False)
        self.scanStacker.removeChannels.setChecked(False)
        self.scanStacker.cancelRemoval.setEnabled(False)
        self.scanStacker.performPolyFit.setEnabled(False)
        self.scanStacker.performRemoval.setEnabled(False)
        self.scanStacker.automaticReduction.setChecked(True)
        self.scanStacker.newOtherPropsFigure.yTFCross.setVisible(True)
        self.mode = 'AUTO'
        self.__updateLabel()
        print("-----> Auto reduction mode is ACTIVE!")
    
    @QtCore.pyqtSlot()
    def __shrtPolyWrapper(self):
        if self.scanStacker.isVisible():
            self.__setPolyFitMode()
        elif self.polEnd.isVisible():
            self.polEnd.setPolyFitMode()
    
    @QtCore.pyqtSlot()
    def __shrtRemWrapper(self):
        if self.scanStacker.isVisible():
            self.__setRemoveChansMode()
        elif self.polEnd.isVisible():
            self.polEnd.setRemoveChansMode()

    @QtCore.pyqtSlot()
    def __shrtAutoWrapper(self):
        if self.scanStacker.isVisible():
            self.__setAutoReductionMode()
        elif self.polEnd.isVisible():
            self.polEnd.setZoomMode()
        
    @QtCore.pyqtSlot()
    def __fitAndPlot(self):
        self.scanStacker.setFitDone()
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __removeAndPlot(self):
        self.data.removeChannels(self.actualBBC, self.actualScanNumber, self.scanStacker.removeChannelsTab)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __cancelRemoval(self):
        self.data.cancelRemoval(self.actualBBC, self.actualScanNumber)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __fitToFinalSpectum(self):
        if len(self.polEnd.fitBoundChannels) != 0:
            ftBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.fitBoundChannels)
            self.polEnd.fitBoundChannels
            self.polEnd.fitBoundChannels
            self.data.finalFitBoundChannels = ftBds
        self.data.fitChebyToFinalSpec(self.actualBBC)
        # -- 
        self.polEnd.setFitDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)
    
    @QtCore.pyqtSlot()
    def __removeOnFinalSpectrum(self):
        if (len(self.polEnd.removeChannelsTab)) != 0:
            rmBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.removeChannelsTab)
            self.data.removeChansOnFinalSpectrum(rmBds)
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrumWOAutoRange(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)
    
    @QtCore.pyqtSlot()
    def __cancelChangesOnFinalSpectrum(self):
        self.data.cancelChangesFinal()
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)

    @QtCore.pyqtSlot()
    def __goToNextPol(self):
        if not self.polEnd.isVisible():
            return

        if self.lhcReduction:
            self.data.clearStack(pol='LHC')
            self.scanStacker.finishPol.setText("  Finish RHC")
            self.polEnd.goToNextPol.setText("  Finish reduction")
            self.lhcReduction = False
            self.scanStacker.autoThreshold = -1e11
        else:
            self.data.clearStack(pol='RHC')
            self.__finishDataReduction()
            self.scanStacker.autoThreshold = -1e11
            return
        
        self.bbcindex += 1
        self.actualBBC = self.BBCs[self.bbcindex]
        self.data.setActualBBC(self.actualBBC)
        self.actualScanNumber = 0
        # --- UI ---
        self.polEnd.setVisible(False)
        self.scanStacker.removeLines()
        self.polEnd.removeLines()
        self.layout.removeWidget(self.polEnd)
        self.layout.addWidget(self.scanStacker)
        self.__plotTimeInfo()
        self.__plotScanNo(self.actualScanNumber)
        self.scanStacker.setVisible(True)
        # ---------
        self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()
    
    @QtCore.pyqtSlot()
    def __finishDataReduction(self):
        self.data.bbcs_used = self.BBCs
        # save fits file
        print("-----------------------------------------")
        self.data.saveReducedDataToFits()
        print("-----> Done!")
        print("-----------------------------------------")
        # disappear
        self.polEnd.setVisible(False)
        self.layout.removeWidget(self.polEnd)
        # plot
        I,V, LHC, RHC = self.data.getFinalPols()
        self.finishW.plotPols(self.data.velTab[self.actualBBC-1], I, V, LHC, RHC)
        # appear
        self.layout.addWidget(self.finishW)
        # -- calibration handling --
        if self.calibrated:
            self.finishW.setYlabel("Flux density (Jy)")
        else:
            self.finishW.setYlabel("Antenna temperature")
        self.finishW.setVisible(True)
    
    @QtCore.pyqtSlot()
    def __closeApp(self):
        if self.finishW.isVisible():
            print("-----> This is the end. Bye!")
            print("-----------------------------------------")
            sys.exit()

    @QtCore.pyqtSlot()
    def __returnToScanEdit(self):
        #UI
        self.polEnd.setVisible(False)
        self.layout.removeWidget(self.polEnd)
        self.layout.addWidget(self.scanStacker, 0, 1)
        self.scanStacker.setVisible(True)
    
    @QtCore.pyqtSlot()
    def __cancelFitOrderChange(self):
        self.orderChanger.setVisible(False)
    
    @QtCore.pyqtSlot()
    def __changeFitOrder(self):
        self.data.setFitOrder(self.orderChanger.getValue())
        self.orderChanger.setVisible(False)
        self.__plotScanNo(self.actualScanNumber)
    
    @QtCore.pyqtSlot()
    def __showFitOrderWidget(self):
        self.orderChanger.setText(self.data.fitOrder)
        self.orderChanger.setVisible(True)

    @QtCore.pyqtSlot()
    def __bbcLhcHandler(self, index):
        for i in range(len(self.changeBBCLHCActions)):
            if i != index:
                self.changeBBCLHCActions[i].setChecked(False)
        self.changeBBCLHCActions[index].setChecked(True)
        self.BBCs[0] = index+1

        if self.lhcReduction:
            self.scanStacker.autoThreshold = -1e11
            self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()
            self.data.clearStackedData()
            self.actualScanNumber = 0
            self.__plotScanNo(self.actualScanNumber)
            self.__plotTimeInfo()
        print(f'-----> BBC for LHC set to {index+1}')

    @QtCore.pyqtSlot()
    def __bbcRhcHandler(self, index):
        for i in range(len(self.changeBBCRHCActions)):
            if i != index:
                self.changeBBCRHCActions[i].setChecked(False)
        self.changeBBCRHCActions[index].setChecked(True)
        self.BBCs[1] = index+1

        if not self.lhcReduction:
            self.scanStacker.autoThreshold = -1e11
            self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()
            self.data.clearStackedData()
            self.actualScanNumber = 0
            self.__plotScanNo(self.actualScanNumber)
            self.__plotTimeInfo()
        print(f'-----> BBC for RHC set to {index+1}')
    
    @QtCore.pyqtSlot()
    def __uncalibrateData(self):
        if self.calibrated:
            spectr = self.data.uncalibrate(self.lhcReduction)
            self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], spectr)
            self.polEnd.setFluxLabel(1)
            self.calibrated = False
            self.polEnd.cancelCalibrations.setEnabled(False)
            self.polEnd.useCalibrations.setEnabled(True)
        else:
            return

    @QtCore.pyqtSlot()
    def __calibrateData(self):
        if not self.calibrated:
            spectr = self.data.calibrate(self.lhcReduction)
            self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], spectr)
            if self.lhcReduction:
                self.polEnd.setFluxLabel(self.data.calCoeffLHC)
            else:
                self.polEnd.setFluxLabel(self.data.calCoeffRHC)
            self.calibrated = True
            self.polEnd.cancelCalibrations.setEnabled(True)
            self.polEnd.useCalibrations.setEnabled(False)
        else:
            return

    @QtCore.pyqtSlot()
    def __showManualCalCoeffWidget(self):
        if self.lhcReduction:
            self.calCoeffChanger.setText(self.data.calCoeffLHC)
        else:
            self.calCoeffChanger.setText(self.data.calCoeffLHC)
        # --
        self.calCoeffChanger.setVisible(True)

    @QtCore.pyqtSlot()
    def __setCalCoeffManually(self):
        # --
        date = self.data.obs.mjd
        calCoeff = self.calCoeffChanger.getValue()
        # --
        # -- prepare: --
        if self.calibrated:
            self.data.uncalibrate(self.lhcReduction)
        # -------------
        if self.lhcReduction:
            self.data.calCoeffLHC = calCoeff
        else:
            self.data.calCoeffRHC = calCoeff
        # --
        spectr = self.data.calibrate(self.lhcReduction)
        # -- plotting --
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], spectr)
        self.polEnd.plotUsedCalCoeff(date, calCoeff)
        if self.lhcReduction:
            self.polEnd.setFluxLabel(self.data.calCoeffLHC)
        else:
            self.polEnd.setFluxLabel(self.data.calCoeffRHC)
        # -- disappear window --
        self.calCoeffChanger.setVisible(False)

    '''
    FOR SHORTCUTS
    '''
    @QtCore.pyqtSlot()
    def __updatePlotAfterFitOrderChange(self):
        if self.scanStacker.isVisible():
            self.__plotScanNo(self.actualScanNumber)
        elif self.polEnd.isVisible():
            self.__fitToFinalSpectum()

    @QtCore.pyqtSlot()
    def __setAutoRangeOnPolEndPlot(self):
        '''
        Sets auto range on polEndPlot
        '''
        if self.polEnd.isVisible():
            self.polEnd.setDefaultRange()
    @QtCore.pyqtSlot()
    def __setFirstOrderPoly(self):
        self.data.setFitOrder(1)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setsecondOrderPoly(self):
        self.data.setFitOrder(2)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setThirdOrderPoly(self):
        self.data.setFitOrder(3)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setFourthOrderPoly(self):
        self.data.setFitOrder(4)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setFifthOrderPoly(self):
        self.data.setFitOrder(5)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setSixthOrderPoly(self):
        self.data.setFitOrder(6)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setSeventhOrderPoly(self):
        self.data.setFitOrder(7)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setEightOrderPoly(self):
        self.data.setFitOrder(8)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setNinthOrderPoly(self):
        self.data.setFitOrder(9)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setTenthOrderPoly(self):
        self.data.setFitOrder(10)
        self.__updatePlotAfterFitOrderChange()
    
    @QtCore.pyqtSlot()
    def doAutoReduction(self):
        '''
        This method is to do automated data reduction
        '''
        if self.scanStacker.autoThreshold == -1e11:
            return False
        
        validationTable = []
        
        for i in self.data.totalFluxTab[self.actualBBC-1]:
            if i < self.scanStacker.autoThreshold:
                validationTable.append(True)
            else:
                validationTable.append(False)
        
        print("-----------------------------------------")
        print("-----> AUTO REDUCTION:")
        for i in range(len(validationTable)):
            if validationTable[i]:
                self.data.addToStack(i)
                print(f"-----> Scan no. {i+1} added")
            else:
                print(f"-----> Scan no. {i+1} discarded")
        print("Automated pol. reduction ended succesfully")
        print("-----------------------------------------")
        return True
    
    @QtCore.pyqtSlot()
    def download_caltabs(self):
        '''
        Downloads caltabs
        '''
        self.data.download_caltabs()
        self.__display_download_caltabs_propmpt(self.data.caltabsLoaded)
        if self.polEnd.isVisible():
            self.__finishPol()

    def __updateLabel(self):
        rms = self.data.calculateFitRMS(self.data.polyTabResiduals)
        snr = self.data.calculateSNR()
        tsys1 = self.data.obs.scans[2*self.actualScanNumber].tsys
        tsys2 = self.data.obs.scans[2*self.actualScanNumber + 1].tsys
        tsys = ((tsys1 + tsys2) / 2.0) / 1000.0
        # tmp
        #rms = 0.15
        #snr = 3.5
        self.scanStacker.setLabel(self.mode, self.data.fitOrder, round(rms,3), self.actualScanNumber+1, len(self.data.obs.mergedScans), round(snr,3), tsys, self.actualBBC)