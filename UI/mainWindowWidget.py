'''
Class, that holds the Main Window of the program
Author: Michał Durjasz
Date: 8.03.2022
'''
from PySide2 import QtCore, QtWidgets, QtGui

# -- class definition starts here --
class mainWindowWidget(QtWidgets.QMainWindow):
    # -- init --
    def __init__(self, parent):
        super().__init__()
        '''
        This is an initialising method. In it, we will place buttons
        and other widgets correctly, by using private methods below:
        '''
        self.__declareAndPlaceButtons()
        #self.__declareAndPlaceCustomWidgets()
        #self.setVisible(True)

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
        self.vboxMain = QtWidgets.QVBoxLayout()
        self.frameForButtons = QtWidgets.QGroupBox("Main operations")
        self.frameForButtons.setLayout(self.vboxMain)
        # buttons
        self.addToStack = QtWidgets.QPushButton("Add to stack") 
        self.discardFromStack = QtWidgets.QPushButton("Discard from stack")
        self.removeChannels = QtWidgets.QPushButton("Remove channels")
        self.fitPolynomial = QtWidgets.QPushButton("Fit Polynomial")
        self.automaticReduction = QtWidgets.QPushButton("Go AUTO")
        # buttons placing
        self.vboxMain.addWidget(self.addToStack)
        self.vboxMain.addWidget(self.discardFromStack)
        self.vboxMain.addWidget(self.removeChannels)
        self.vboxMain.addWidget(self.fitPolynomial)
        self.vboxMain.addWidget(self.automaticReduction)
        # layouts placing
        self.layout.addWidget(self.frameForButtons, 0,0)
        # buttons sizing
        self.addToStack.setMaximumSize(10000, 10000)
        self.addToStack.setMinimumSize(0, 0)
        self.discardFromStack.setMaximumSize(10000, 10000)
        self.discardFromStack.setMinimumSize(0, 0)
        self.removeChannels.setMaximumSize(10000, 10000)
        self.removeChannels.setMinimumSize(0, 0)
        self.fitPolynomial.setMaximumSize(10000, 10000)
        self.fitPolynomial.setMinimumSize(0, 0)
        self.automaticReduction.setMaximumSize(10000, 10000)
        self.automaticReduction.setMinimumSize(0, 0)
        # buttons colors
        self.addToStack.setStyleSheet("background-color: green")
        self.discardFromStack.setStyleSheet("background-color: red")