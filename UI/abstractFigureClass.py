'''
This is base template << abstract >> figure class
it is used as a base for mode advanced figure classes
it provides base functionalities:
-> figure
-> makeFancyTicks
User has to make ax and plots separately (this is only base template)
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

class templateFigure(FigureCanvasQTAgg):
    def __init__(self):
        self.figure = plt.figure()
        super(templateFigure, self).__init__(self.figure)

    def makeFancyTicks(self, ax):
        ax.xaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 5, top=True, right=True, left=True, bottom = True)
        ax.yaxis.set_tick_params(direction='in', width=1, length = 3,which='minor', top=True, right=True, left=True, bottom = True)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    
    def autoscaleAxis(self, ax, tight=False):
        ax.relim()
        if tight:
            ax.autoscale(axis='x', tight=True)
            ax.autoscale(axis='y', tight=False)
        else:
            ax.autoscale()
    
    def drawF(self):
        self.figure.canvas.draw_idle()