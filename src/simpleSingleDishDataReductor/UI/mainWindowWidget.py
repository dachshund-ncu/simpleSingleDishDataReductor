"""
Class, that holds the Main Window of the program
Author: Michał Durjasz
Date: 8.03.2022
"""
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMenuBar

from simpleSingleDishDataReductor.UI.ui_elements import custom_menu

from .scanStackingWidget import scanStackingWidget
from .polEndWidget import polEndWidget
from .finishWidget import finishWidgetP
from .fitOrderChangeWidget import changeOrder
from .manualCalCoeffSetter import changeCalCoeffWindow
from .ui_elements.custom_menu import CustomMenu
from .ui_elements import style_sheet
import os
import numpy as np
import sys
import functools as fctls
from simpleSingleDishDataReductor.data.dataClass import dataContainter
from simpleSingleDishDataReductor.UI.icons import satellite_dish


# -- class definition starts here --
class mainWindowWidget(QtWidgets.QMainWindow):
    # -- init --
    def __init__(
            self,
            software_path: str | None = None,
            target_filename: str | None = None,
            is_on_off: bool = False,
            calibrate: bool = True):
        super().__init__()
        self.setVisible(False)
        self.setStyleSheet(style_sheet)

        # -- initialize default parameters --
        self.__initialize_data_reduction_parameters()

        # -- parameters --
        self.software_path = software_path
        self.target_filename = target_filename
        self.is_on_off = is_on_off
        self.calibrate = calibrate
        self.data = self.__load_data_from_filename(
            software_path=self.software_path,
            target_filename=self.target_filename,
            is_on_off=self.is_on_off)

        # -- initialize ui elements
        self.__declareAndPlaceButtons()
        self.__declareMenu()
        self.__declareAndPlaceCustomWidgets()
        self.__connectButtonsToSlots()


        self.__display_initial_informations()

        self.setWindowIcon(satellite_dish)
        self.resize(1366, 720)
        self.setVisible(True)


        if self.data is not None and len(self.data.caltabs) < 1:
            self.display_caltab_prompt("Seems there are no downloaded caltabs. Would you like to download them?")

    def __load_data_from_filename(
            self,
            software_path: str | None = None,
            target_filename: str | None = None,
            is_on_off: bool = False) -> dataContainter | None:
        if software_path is None:
            return None
        if target_filename is None:
            return None
        data = dataContainter(
            software_path=software_path,
            target_filename=target_filename,
            onOff=is_on_off)
        self.__initialize_data_reduction_parameters()
        return data

    def __set_window_title(self):
        if self.data is not None:
            self.setWindowTitle("Data reduction: " \
                                + self.data.obs.scans[0].sourcename \
                                + " " \
                                + self.data.obs.scans[0].isotime)

    def __initialize_data_reduction_parameters(self):
        self.calibrated = False
        self.BBCs = [3,2]
        self.bbcindex = 0
        self.lhcReduction = True
        self.actualScanNumber = 0
        self.actualBBC = self.BBCs[0]
        self.timeInfoAlreadyPlotted = False
        self.mode: str | None = None

    def __display_initial_informations(self):
        if self.data is not None:
            self.__reset_ui()
            self.maximumScanNumber = len(self.data.obs.mergedScans)
            self.__plotTimeInfo()
            self.__plotScanNo(self.actualScanNumber)
            self.__setPolyFitMode()
            self.__add_bbc_menus()
            self.__connect_bbc_menus()
            self.__setCheckedBBCActions()


    @QtCore.pyqtSlot()
    def __load_file_from_gui(self) -> None:
        # 'self' is usually your QMainWindow or QWidget
        file_filter = "Observation archive (*.tar.bz2);;All files (*.*)"

        # getOpenFileName returns a tuple: (absolute_path, selected_filter)
        absolute_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption="Select archive (.tar.bz2)",
            directory="",
            filter=file_filter,
            initialFilter="Observation archive (*.tar.bz2)"
        )

        if not absolute_path: return
        self.target_filename = absolute_path
        self.data = self.__load_data_from_filename(
            software_path=self.software_path,
            target_filename=self.target_filename,
            is_on_off=self.is_on_off)
        self.__display_initial_informations()

    @QtCore.pyqtSlot()
    def __reload_data(self) -> None:
        self.data = self.__load_data_from_filename(
            software_path=self.software_path,
            target_filename=self.target_filename,
            is_on_off=self.is_on_off)
        self.__display_initial_informations()


    def __reset_ui(self) -> None:
        self.__delete_bbc_menus()
        self.lhcReduction = True
        self.scanStacker.finishPol.setText("  Finish LHC")
        self.polEnd.goToNextPol.setText("  Finish polarization")
        self.changeBbcLhc.setEnabled(True)
        self.changeBbcRhc.setEnabled(True)
        self.scanStacker.reset_plots()
        self.scanStacker.perform_automated_reduction.setEnabled(False)
        self.scanStacker.autoThreshold = None
        self.__show_scan_stacker()


    def __show_scan_stacker(self):
        self.polEnd.setVisible(False)
        self.finishW.setVisible(False)
        self.scanStacker.setVisible(True)

    def __declareAndPlaceButtons(self):
        """
        This methood will declare and place buttons correctly. There
        is also declared layout (QGrid) and primary widget(window), so watch out for that.
        Maybe it would be better to declare it separately?
        Buttons will be placed in the groupBoxes
        """
        # layouts
        self.window = QtWidgets.QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QtWidgets.QGridLayout(self.window)
        # shortcuts
        self.firstOrderFit = QtGui.QShortcut(QtGui.QKeySequence('1'), self)
        self.secondOrderFit = QtGui.QShortcut(QtGui.QKeySequence('2'), self)
        self.thirdOrderFit = QtGui.QShortcut(QtGui.QKeySequence('3'), self)
        self.fourthOrderFit = QtGui.QShortcut(QtGui.QKeySequence('4'), self)
        self.fifthtOrderFit = QtGui.QShortcut(QtGui.QKeySequence('5'), self)
        self.sixthOrderFit = QtGui.QShortcut(QtGui.QKeySequence('6'), self)
        self.seventhOrderFit = QtGui.QShortcut(QtGui.QKeySequence('7'), self)
        self.eighthOrderFit = QtGui.QShortcut(QtGui.QKeySequence('8'), self)
        self.ninthOrderFit = QtGui.QShortcut(QtGui.QKeySequence('9'), self)
        self.tenthOrderFit = QtGui.QShortcut(QtGui.QKeySequence('t'), self)
        self.shrtAddToStack = QtGui.QShortcut(QtGui.QKeySequence('k'), self)
        self.shrtDiscardToStack = QtGui.QShortcut(QtGui.QKeySequence('d'), self)
        self.shrtNextScan = QtGui.QShortcut(QtGui.QKeySequence('right'), self)
        self.shrtPrevScan = QtGui.QShortcut(QtGui.QKeySequence('left'), self)
        self.shrtNextPol = QtGui.QShortcut(QtGui.QKeySequence('n'), self)
        self.shrtEndRed = QtGui.QShortcut(QtGui.QKeySequence('p'), self)
        self.shrtremoveChansMode = QtGui.QShortcut(QtGui.QKeySequence('r'), self)
        self.shrtfitPolyMode = QtGui.QShortcut(QtGui.QKeySequence('f'), self)
        self.shrtAutoRedMode = QtGui.QShortcut(QtGui.QKeySequence('i'), self)
        self.setDefaultRangeOnPolEndShrt = QtGui.QShortcut(QtGui.QKeySequence('b'), self)
        self.perform_auto_reduction_shortcut = QtGui.QShortcut(QtGui.QKeySequence('a'), self)

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
        self.layout.addWidget(self.polEnd, 0, 1, 2, 1)
        self.layout.addWidget(self.finishW, 0, 1, 2, 1)

    def __add_bbc_menus(self):
        if self.data is not None:
            for i in range(len(self.data.obs.mergedScans[0].pols)):
                lhc_action = QtGui.QAction(f"BBC {i + 1}", self)
                rhc_action = QtGui.QAction(f"BBC {i + 1}", self)

                lhc_action.setCheckable(True)
                rhc_action.setCheckable(True)

                self.changeBBCLHCActions.append(lhc_action)
                self.changeBBCRHCActions.append(rhc_action)

                self.changeBbcLhc.addAction(lhc_action)
                self.changeBbcRhc.addAction(rhc_action)

    def __delete_bbc_menus(self):
        """
        Cleans up BBC actions from the UI, disconnects triggers,
        and clears the tracking lists.
        """
        # Helper to clean a specific menu and its tracking list
        def reset_menu(menu_widget: custom_menu, actions_list):
            for action in actions_list:
                menu_widget.removeAction(action)
            actions_list.clear()
        reset_menu(self.changeBbcLhc, self.changeBBCLHCActions)
        reset_menu(self.changeBbcRhc, self.changeBBCRHCActions)

    def __declare_advanced_menu(self) -> None:
        self.advanced_menu = CustomMenu("Advanced", self)
        self.advanced_menu.setTitle("Advanced")  # Set the visible name on the bar
        self.advanced_menu.setToolTip("Advanced settings")
        # Change Fit Order Action
        self.changeOrderAction = QtGui.QAction("Change fit order", self)
        self.advanced_menu.addAction(self.changeOrderAction)
        # Submenus for BBC
        self.changeBbcLhc = self.advanced_menu.addMenu("BBC for LHC")
        self.changeBbcRhc = self.advanced_menu.addMenu("BBC for RHC")

        self.changeBBCLHCActions = []
        self.changeBBCRHCActions = []

        # -- advanced tinkers --
        self.is_on_off_action = QtGui.QAction("On-off data reduction", self)
        self.is_on_off_action.setCheckable(True)
        self.is_on_off_action.setChecked(self.is_on_off)

        # -- Caltab and JSON loading
        self.advanced_menu.addAction(self.is_on_off_action)
        self.advanced_menu.addSeparator()
        self.download_caltabs_a = QtGui.QAction("Download caltabs", self)
        self.save_scans_to_json_a = QtGui.QAction("Save scans to json", self)

        self.advanced_menu.addAction(self.download_caltabs_a)
        self.advanced_menu.addSeparator()
        self.advanced_menu.addAction(self.save_scans_to_json_a)

    def __declare_file_menu(self) -> None:
        # declare
        self.file_menu = CustomMenu("File", self)
        self.file_menu.setTitle("File")  # Set the visible name on the bar
        self.file_menu.setToolTip("File options")
        # declare actions
        self.load_file_menu_a = QtGui.QAction("Load archive", self)
        self.reload_file_menu_a = QtGui.QAction("Reload archive", self)
        self.quit_file_menu_a = QtGui.QAction("Quit", self)
        # add to menu
        self.file_menu.addAction(self.load_file_menu_a)
        self.file_menu.addAction(self.reload_file_menu_a)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_file_menu_a)

    def __declareMenu(self):
        """
        This method declares the menu and adds it to the window's Menu Bar
        """
        # Create the menu bar (or get the existing one)
        menubar: QMenuBar = self.menuBar()
        # -- advanced menu --
        self.__declare_advanced_menu()
        self.__declare_file_menu()

        menubar.addMenu(self.file_menu)
        menubar.addMenu(self.advanced_menu)

    def __setCheckedBBCActions(self):
        """
        This method sets checked actions for BBCs
        We want only the 1 BBC per pol to be checked
        We manage that by executing the code below
        self.BBCs is the list of used BBCs: by default these are [1,2]
        """
        if self.data is not None:
            self.changeBBCLHCActions[self.BBCs[0]-1].setChecked(True)
            self.changeBBCRHCActions[self.BBCs[1]-1].setChecked(True)


    def __connectButtonsToSlots(self):
        """
        This method connects buttons and actions to the corresponding slots
        """
        # -- file menu --
        self.quit_file_menu_a.triggered.connect(self.__close_app_from_menu)
        # -- scan stacker --
        self.scanStacker.nextScan.triggered.connect(self.__nextScanSlot)
        self.scanStacker.prevScan.triggered.connect(self.__prevScanSlot)
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
        self.scanStacker.perform_automated_reduction.clicked.connect(self.__perform_auto_reduction)

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
        # -- automated shortducts --
        self.perform_auto_reduction_shortcut.activated.connect(self.__perform_auto_reduction)
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
        self.save_scans_to_json_a.triggered.connect(self.__save_scans_to_json)
        self.polEnd.save_to_json_btn.clicked.connect(self.__save_final_spectrum_to_json)

        # -- connect actions --
        self.load_file_menu_a.triggered.connect(self.__load_file_from_gui)
        self.reload_file_menu_a.triggered.connect(self.__reload_data)
        self.is_on_off_action.triggered.connect(self.toggle_on_off)

    def __connect_bbc_menus(self):
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
        if self.data is None: return
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

    def display_message(self, text: str) -> None:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Message")
        msgBox.setText(text)
        msgBox.exec()

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
        if self.data is None: return
        if self.actualScanNumber+1 < self.maximumScanNumber:
            self.actualScanNumber += 1
        else:
            self.actualScanNumber = 0

        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __prevScanSlot(self):
        if self.data is None: return
        if self.actualScanNumber-1 >= 0:
            self.actualScanNumber -= 1
        else:
            self.actualScanNumber = self.maximumScanNumber-1

        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __perform_auto_reduction(self) -> None:
        if not self.scanStacker.isVisible(): return
        if self.scanStacker.autoThreshold is None:
            return
        if not self.scanStacker.autoRedMode:
            return
        flag = self.doAutoReduction()
        if flag:
            self.__finishPol()
            return

    @QtCore.pyqtSlot()
    def __addToStackSlot(self) -> None:
        """
        Adds to stack of reduced spectra
        'STACK' is being averaged, what gives better and better SNR with every addition
        """
        if self.data is None: return
        if not self.scanStacker.isVisible():
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
        if self.data is None: return
        self.data.deleteFromStack(self.actualScanNumber)
        self.scanStacker.newOtherPropsFigure.setTotalFluxDiscarded(self.actualScanNumber)
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __finishPol(self):
        if self.data is None: return
        # UI
        self.scanStacker.setVisible(False)
        # self.layout.removeWidget(self.scanStacker)
        # self.layout.addWidget(self.polEnd, 0, 1)
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
        if self.data.properCaltabIndex >= len(self.data.caltabs) and self.calibrate:
            self.display_message(f"Did not find caltab, that match rest frequency of {round(self.data.obs.scans[0].rest[0] / 1000.0, 5)} GHz")
            return
        if not flag_cal and self.calibrate:
            self.display_caltab_prompt(
                f"Seems that the calibration tables are too short."
                + f"\nLast epoch in {self.data.caltabs[self.data.properCaltabIndex].label} "
                + f"is {self.data.caltabs[self.data.properCaltabIndex].getMaxEpoch()}, "
                + f"while epoch of this obs. is {round(self.data.obs.mjd,3)}.\nWould you like to download them?")

    @QtCore.pyqtSlot()
    def __save_scans_to_json(self):
        """
        Simply save loaded scans to txt file
        """
        if self.data is None: return
        saved_filename = self.data.save_scans_to_json()
        self.display_message(text=f"Saved scans to file:{saved_filename}")

    @QtCore.pyqtSlot()
    def __save_final_spectrum_to_json(self):
        if self.data is None: return
        saved_filename  = self.data.save_final_spectrum_to_json()
        self.display_message(text=f"Saved final spectrum to file:{saved_filename}")

    @QtCore.pyqtSlot()
    def __discardScan(self):
        if self.data is None: return
        self.data.discardFromStack(self.actualScanNumber)
        self.scanStacker.newOtherPropsFigure.setTotalFluxDiscarded(self.actualScanNumber)
        if self.data.checkIfAllScansProceeded():
            self.__plotScanNo(self.actualScanNumber)
            self.__finishPol()
        else:
            self.__nextScanSlot()

    @QtCore.pyqtSlot()
    def __setPolyFitMode(self):
        if self.data is None: return
        # self.scanStacker.polyFitMode = True
        self.scanStacker.set_mode("polyfit")
        self.mode = 'Polynomial fit'
        self.__updateLabel()
        print("-----> Polynomial fit mode is ACTIVE!")

    @QtCore.pyqtSlot()
    def __setRemoveChansMode(self):
        if self.data is None: return
        self.scanStacker.set_mode("remove")
        self.scanStacker.setBoundChannels(self.data.fitBoundsChannels)
        self.mode = 'Remove channels'
        self.__updateLabel()
        print("-----> Channel removal mode is ACTIVE!")

    @QtCore.pyqtSlot()
    def __setAutoReductionMode(self):
        if self.data is None: return
        self.scanStacker.set_mode("auto")

        self.mode = 'AUTO'
        self.__updateLabel()
        print("-----> Auto reduction mode is ACTIVE!")

    @QtCore.pyqtSlot()
    def __shrtPolyWrapper(self):
        if self.data is None: return
        if self.scanStacker.isVisible():
            self.__setPolyFitMode()
        elif self.polEnd.isVisible():
            self.polEnd.setPolyFitMode()

    @QtCore.pyqtSlot()
    def __shrtRemWrapper(self):
        if self.data is None: return
        if self.scanStacker.isVisible():
            self.__setRemoveChansMode()
        elif self.polEnd.isVisible():
            self.polEnd.setRemoveChansMode()

    @QtCore.pyqtSlot()
    def __shrtAutoWrapper(self):
        if self.data is None: return
        if self.scanStacker.isVisible():
            self.__setAutoReductionMode()
        elif self.polEnd.isVisible():
            self.polEnd.setZoomMode()

    @QtCore.pyqtSlot()
    def __fitAndPlot(self):
        if self.data is None: return
        self.scanStacker.setFitDone()
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __removeAndPlot(self):
        if self.data is None: return
        self.data.removeChannels(self.actualBBC, self.actualScanNumber, self.scanStacker.removeChannelsTab)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __cancelRemoval(self):
        if self.data is None: return
        self.data.cancelRemoval(self.actualBBC, self.actualScanNumber)
        self.scanStacker.setRemoveDone()
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __fitToFinalSpectum(self):
        if self.data is None: return
        if len(self.polEnd.fitBoundChannels) != 0:
            ftBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.fitBoundChannels)
            self.data.finalFitBoundChannels = ftBds
        self.data.fitChebyToFinalSpec(self.actualBBC)
        # --
        self.polEnd.setFitDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)

    @QtCore.pyqtSlot()
    def __removeOnFinalSpectrum(self):
        if self.data is None: return
        if (len(self.polEnd.removeChannelsTab)) != 0:
            rmBds = self.data.convertVelsToChannels(self.actualBBC-1, self.polEnd.removeChannelsTab)
            self.data.removeChansOnFinalSpectrum(rmBds)
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrumWOAutoRange(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)

    @QtCore.pyqtSlot()
    def __cancelChangesOnFinalSpectrum(self):
        if self.data is None: return
        self.data.cancelChangesFinal()
        self.polEnd.setRemoveDone()
        self.polEnd.plotSpectrum(self.data.velTab[self.actualBBC-1], self.data.finalFitRes)

    @QtCore.pyqtSlot()
    def __goToNextPol(self):
        if self.data is None: return
        if not self.polEnd.isVisible():
            return
        if self.lhcReduction:
            self.data.clearStack(pol='LHC')
            self.scanStacker.finishPol.setText("  Finish RHC")
            self.polEnd.goToNextPol.setText("  Finish reduction")
            self.lhcReduction = False
            self.scanStacker.autoThreshold = None
        else:
            self.data.clearStack(pol='RHC')
            self.__finishDataReduction()
            self.scanStacker.autoThreshold = None
            return

        self.scanStacker.autoThrshold = None
        self.scanStacker.perform_automated_reduction.setEnabled(False)
        self.bbcindex += 1
        self.actualBBC = self.BBCs[self.bbcindex]
        self.data.setActualBBC(self.actualBBC)
        self.actualScanNumber = 0
        # --- UI ---
        self.polEnd.setVisible(False)
        self.scanStacker.removeLines()
        self.polEnd.removeLines()
        # self.layout.removeWidget(self.polEnd)
        # self.layout.addWidget(self.scanStacker)
        self.__plotTimeInfo()
        self.__plotScanNo(self.actualScanNumber)
        self.scanStacker.setVisible(True)
        # ---------
        self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()

    @QtCore.pyqtSlot()
    def __finishDataReduction(self):
        if self.data is None: return
        self.data.bbcs_used = self.BBCs
        # save fits file
        print("-----------------------------------------")
        self.data.saveReducedDataToFits()
        print("-----> Done!")
        print("-----------------------------------------")
        # disappear
        self.polEnd.setVisible(False)
        # self.layout.removeWidget(self.polEnd)
        # plot
        I,V, LHC, RHC = self.data.getFinalPols()
        self.finishW.plotPols(self.data.velTab[self.actualBBC-1], I, V, LHC, RHC)
        # appear
        # self.layout.addWidget(self.finishW)
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
    def __close_app_from_menu(self):
        sys.exit()

    @QtCore.pyqtSlot()
    def __returnToScanEdit(self):
        if self.data is None: return
        #UI
        self.polEnd.setVisible(False)
        # self.layout.removeWidget(self.polEnd)
        # self.layout.addWidget(self.scanStacker, 0, 1)
        self.scanStacker.setVisible(True)

    @QtCore.pyqtSlot()
    def __cancelFitOrderChange(self):
        self.orderChanger.setVisible(False)

    @QtCore.pyqtSlot()
    def __changeFitOrder(self):
        if self.data is None: return
        self.data.setFitOrder(self.orderChanger.getValue())
        self.orderChanger.setVisible(False)
        self.__plotScanNo(self.actualScanNumber)

    @QtCore.pyqtSlot()
    def __showFitOrderWidget(self):
        if self.data is None: return
        self.orderChanger.setText(self.data.fitOrder)
        self.orderChanger.setVisible(True)

    @QtCore.pyqtSlot()
    def __bbcLhcHandler(self, index):
        if self.data is None: return
        for i in range(len(self.changeBBCLHCActions)):
            if i != index:
                self.changeBBCLHCActions[i].setChecked(False)
        self.changeBBCLHCActions[index].setChecked(True)
        self.BBCs[0] = index+1

        if self.lhcReduction:
            self.scanStacker.autoThreshold = None
            self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()
            self.scanStacker.perform_automated_reduction.setEnabled(False)
            self.data.clearStackedData()
            self.actualScanNumber = 0
            self.__plotScanNo(self.actualScanNumber)
            self.__plotTimeInfo()
        print(f'-----> BBC for LHC set to {index+1}')

    @QtCore.pyqtSlot()
    def __bbcRhcHandler(self, index):
        if self.data is None: return
        for i in range(len(self.changeBBCRHCActions)):
            if i != index:
                self.changeBBCRHCActions[i].setChecked(False)
        self.changeBBCRHCActions[index].setChecked(True)
        self.BBCs[1] = index+1

        if not self.lhcReduction:
            self.scanStacker.autoThreshold = None
            self.scanStacker.newOtherPropsFigure.setTotalFluxDefaultBrush()
            self.scanStacker.perform_automated_reduction.setEnabled(False)
            self.data.clearStackedData()
            self.actualScanNumber = 0
            self.__plotScanNo(self.actualScanNumber)
            self.__plotTimeInfo()
        print(f'-----> BBC for RHC set to {index+1}')

    @QtCore.pyqtSlot()
    def __uncalibrateData(self):
        if self.data is None: return
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
        if self.data is None: return
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
        if self.data is None: return
        if self.lhcReduction:
            self.calCoeffChanger.setText(self.data.calCoeffLHC)
        else:
            self.calCoeffChanger.setText(self.data.calCoeffLHC)
        # --
        self.calCoeffChanger.setVisible(True)

    @QtCore.pyqtSlot()
    def __setCalCoeffManually(self):
        if self.data is None: return
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
        if self.data is None: return
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
        if self.data is None: return
        self.data.setFitOrder(1)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setsecondOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(2)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setThirdOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(3)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setFourthOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(4)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setFifthOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(5)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setSixthOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(6)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setSeventhOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(7)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setEightOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(8)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setNinthOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(9)
        self.__updatePlotAfterFitOrderChange()
    @QtCore.pyqtSlot()
    def __setTenthOrderPoly(self):
        if self.data is None: return
        self.data.setFitOrder(10)
        self.__updatePlotAfterFitOrderChange()


    @QtCore.pyqtSlot()
    def doAutoReduction(self):
        """
        This method is to do automated data reduction
        """
        if self.data is None: return
        if self.scanStacker.autoThreshold is None:
            return False

        validation_table = []
        for i in self.data.totalFluxTab[self.actualBBC-1]:
            if i < self.scanStacker.autoThreshold:
                validation_table.append(True)
            else:
                validation_table.append(False)

        print("-----------------------------------------")
        print("-----> AUTO REDUCTION:")
        for i in range(len(validation_table)):
            if validation_table[i]:
                self.data.addToStack(i)
                print(f"-----> Scan no. {i+1} added")
            else:
                print(f"-----> Scan no. {i+1} discarded")
        print("Automated pol. reduction ended succesfully")
        print("-----------------------------------------")
        return True

    @QtCore.pyqtSlot()
    def download_caltabs(self):
        """
        Downloads caltabs
        """
        if self.data is None: return
        self.data.download_caltabs()
        self.__display_download_caltabs_propmpt(self.data.caltabsLoaded)
        if self.polEnd.isVisible():
            self.__finishPol()

    def __updateLabel(self):
        if self.data is not None:
            rms = self.data.calculateFitRMS(self.data.polyTabResiduals)
            snr = self.data.calculateSNR()
            tsys1 = self.data.obs.scans[2*self.actualScanNumber].tsys
            tsys2 = self.data.obs.scans[2*self.actualScanNumber + 1].tsys
            tsys = ((tsys1 + tsys2) / 2.0) / 1000.0
            # tmp
            #rms = 0.15
            #snr = 3.5
            self.scanStacker.setLabel(self.mode, self.data.fitOrder, round(rms,3), self.actualScanNumber+1, len(self.data.obs.mergedScans), round(snr,3), tsys, self.actualBBC)

    @QtCore.pyqtSlot()
    def toggle_on_off(self):
        self.is_on_off = self.is_on_off_action.isChecked()
        self.__reload_data()