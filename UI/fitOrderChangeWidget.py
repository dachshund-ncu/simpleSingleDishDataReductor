'''
VERY smol widget, that holds simple UI for changing fit order
'''

from PySide2 import QtWidgets
from customButton import cButton

class changeOrder(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)
        self.cancel = cButton("Cancel")
        self.apply = cButton("Set")
        self.textEdit = QtWidgets.QSpinBox(self)
        self.layout.addWidget(self.textEdit, 0,0,1,2)
        self.layout.addWidget(self.cancel, 1,0)
        self.layout.addWidget(self.apply, 1,1)
        
    
    def setText(self, value):
        self.textEdit.setValue(value)
    
    def getValue(self):
        return int(self.textEdit.cleanText())