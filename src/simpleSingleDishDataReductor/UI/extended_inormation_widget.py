from .ui_elements.custom_widget import custom_widget
from icons import gears_icon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class extended_information_widget(custom_widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 500, 800)
        self.initialize_layout()
        self.setWindowTitle("Extended information")
        self.setWindowIcon(gears_icon)
        self.setVisible(False)

    def initialize_layout(self) -> None:
        self.layout = QVBoxLayout(self)
        self.text_editor = QTextEdit(self)
        self.text_editor.setReadOnly(True)
        self.text_editor.setText("")
        self.layout.addWidget(self.text_editor)

    def set_text(self, text: str) -> None:
        self.text_editor.setText(text)