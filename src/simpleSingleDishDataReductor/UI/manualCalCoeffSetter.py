"""
VERY smol widget, that holds simple UI for changing cal coefficient
"""
from PyQt5 import QtWidgets
from .ui_elements.customButton import custom_button


class changeCalCoeffWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)
        self.setStyleSheet('''
        QWidget {
            background-color: #121212;
            border-radius: 10px;
            padding: 0px;
            font-size: 15px;
            margin-left: 0px;
            margin-right: 0px;
            margin-top: 0px;
            margin-bottom: 0px;
        }
        QDoubleSpinBox {
            background-color: rgba(255,255,255,5%);
            color: white; /* text color */
            padding: 4px; /* padding */
            font-size: 15px; /* font size */
            border-radius: 8px; /* border radius */
            text-align: left;
            font-family: silka;
            padding: 8px 12px;
        }
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            background-color: transparent;
            color: red; /* text color */
            border: 1px solid rgba(255,255,255,5%);
            padding: 2px;
        }
        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed  {
            background-color: #C2185B;
        }
        QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
            color: white; /* text color */
            padding: 2px;
        }
        ''')
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