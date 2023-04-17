import pyqtgraph as pg
import numpy as np

from rt_formant.sound import BUFF_SIZE, SAMPLING_RATE
from rt_formant.signal import normalized_fft


xgraph = np.linspace(0, SAMPLING_RATE, BUFF_SIZE)


class FFT:
    def __init__(self, plot_item: pg.PlotItem):
        self.plot_item = plot_item

    def update(self, data):
        freq = np.abs(normalized_fft(data))
        y = [freq]
        self.plot_item.clear()
        self.plot_item.setLogMode(False, True)
        self.plot_item.setXRange(0, 8000, padding = 0)
        self.plot_item.setYRange(-6, 0, padding = 0)
        self.plot_item.multiDataPlot(x=xgraph, y=y, pen="green")
