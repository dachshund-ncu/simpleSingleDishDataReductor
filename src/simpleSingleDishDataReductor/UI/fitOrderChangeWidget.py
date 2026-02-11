"""
VERY smol widget, that holds simple UI for changing fit order
"""

from PyQt5 import QtWidgets
from .ui_elements.customButton import custom_button

class changeOrder(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        QSpinBox {
            background-color: rgba(255,255,255,5%);
            color: white; /* text color */
            padding: 4px; /* padding */
            font-size: 15px; /* font size */
            border-radius: 8px; /* border radius */
            text-align: left;
            font-family: silka;
            padding: 8px 12px;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: transparent;
            color: red; /* text color */
            border: 1px solid rgba(255,255,255,5%);
            padding: 2px;
        }
        QSpinBox::up-button:pressed, QSpinBox::down-button:pressed  {
            background-color: #C2185B;
        }
        QSpinBox::up-arrow, QSpinBox::down-arrow {
            color: white; /* text color */
            padding: 2px;
        }
        ''')
        self.setVisible(False)
        self.layout = QtWidgets.QGridLayout(self)

        self.cancel = custom_button("Cancel")
        self.apply = custom_button("Set")
        self.textEdit = QtWidgets.QSpinBox(self)
        self.layout.addWidget(self.textEdit, 0,0,1,2)
        self.layout.addWidget(self.cancel, 1,0)
        self.layout.addWidget(self.apply, 1,1)
        
    
    def setText(self, value):
        self.textEdit.setValue(value)
    
    def getValue(self):
        return int(self.textEdit.cleanText())