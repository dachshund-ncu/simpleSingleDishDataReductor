from PyQt5.QtWidgets import QLabel

class custom_label(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)

        self.setStyleSheet(
            "\
                QLabel { \
                    background-color: transparent;\
                    padding: 0px;\
                    text-align: center;\
                    color: white; /* text color */\
                    font-size: 14px; /* font size */\
                    font-family: silka;\
                }\
            ")
    def setBackgroundColor(self, color):
        self.setStyleSheet(
            "\
                QLabel { \
                    background-color: %s;\
                    padding: 0px;\
                    text-align: center;\
                    color: white; /* text color */\
                    font-size: 14px; /* font size */\
                    font-family: silka;\
                }\
            " % color)
