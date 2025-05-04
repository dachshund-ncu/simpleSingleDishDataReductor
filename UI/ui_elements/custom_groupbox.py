from PyQt5 import QtWidgets

class custom_gb_see_th(QtWidgets.QGroupBox):
    def __init__(self, *args):
        QtWidgets.QGroupBox.__init__(self, *args)
        self.setStyleSheet('''
                QGroupBox {
                    color: #BB86FC; /* text color */
                    background-color: transparent ;
                    font-size: 2; /* font size */
                    border-radius: 10px; /* border radius */
                    
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0px;
                }
                QWidget{
                    background-color: rgba(255, 255, 255, 3%);
                    border-radius: 10px;
                    font-size: 2; /* font size */
                }
            ''')