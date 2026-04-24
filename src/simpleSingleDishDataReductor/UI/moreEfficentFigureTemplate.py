"""
More efficcient figure template in pyQtGraph
"""
import pyqtgraph as pg
class templateFigurePG(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground(None)
        self.setStyleSheet("background-color: transparent;")
        # self.setBackground(pg.mkColor(255, 255, 255, 100))