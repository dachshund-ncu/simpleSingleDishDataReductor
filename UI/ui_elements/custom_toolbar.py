from PyQt5.QtWidgets import QToolBar

class CustomToolbar(QToolBar):
    def __init__(self, *args):
        QToolBar.__init__(self, *args)
        self.setStyleSheet("""
            QWidget{
                background-color: transparent;
            }
            QToolButton {
                background-color: transparent; /* background color */
                color: white; /* text color */
                padding: 4px; /* padding */
                font-size: 15px; /* font size */
                border-radius: 8px; /* border radius */
                text-align:left;
                font-family: silka;
            }

            QToolButton:hover {
                background-color: rgba(255,255,255,12%);
            }
            QToolButton:pressed {
                background-color: rgba(255,255,255,15%);
            }
            QToolButton:checked {
                background-color: rgba(255,255,255,20%);
            }
            QToolTip {
                background-color: #141414;
                color: white; /* text color */
                padding: 4px; /* padding */
                font-size: 14px; /* font size */
                border-radius: 4px; /* border radius */
                text-align:left;
                font-family: silka;
            }
        """)
