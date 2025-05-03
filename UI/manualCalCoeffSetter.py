'''
VERY smol widget, that holds simple UI for changing cal coefficient
'''
from PyQt5 import QtWidgets
from .ui_elements.customButton import custom_button


class changeCalCoeffWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.cancel = custom_button("Cancel")
        self.apply = custom_button("Set")
        self.textEdit = QtWidgets.QDoubleSpinBox(self)
        self.layout.addWidget(self.textEdit, 0,0,1,2)
        self.layout.addWidget(self.cancel, 1,0)
        self.layout.addWidget(self.apply, 1,1)
        self.cancel.clicked.connect(self.__disappearThis)
    
    def setText(self, value):
        self.textEdit.setValue(value)
    
    def getValue(self):
        text = self.textEdit.cleanText() 
        return self.textEdit.valueFromText(text)     

    def __disappearThis(self):
        self.setVisible(False)