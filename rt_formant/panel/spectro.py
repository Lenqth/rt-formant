import pyqtgraph as pg
import numpy as np
import scipy
import sys
from rt_formant.sound import BUFF_SIZE, SAMPLING_RATE
from rt_formant.signal import normalized_fft

SPECTRO_HISTORY_SIZE = 60

class Spectrogram:
    def __init__(self, plot_item: pg.PlotItem):
        self.plot_item = plot_item
        self.spectrogram = np.zeros(
            shape = (SPECTRO_HISTORY_SIZE, BUFF_SIZE)
        )
        cmap = pg.colormap.getFromMatplotlib("gray")
        self.im = pg.ImageItem(border="k", cmap=cmap)

        self.plot_item.setYRange(0, SAMPLING_RATE / 2, padding = 0)
        self.plot_item.setXRange(0, SPECTRO_HISTORY_SIZE, padding = 0)
        
        plot_item.addItem(self.im)
        plot_item.addColorBar( self.im, colorMap='gray', values=(-4, -2) )

    def update(self, data):
        freq = np.abs(normalized_fft(data))
        
        self.spectrogram[:-1, :] = self.spectrogram[1:, :]
        self.spectrogram[-1, :] = np.log10(freq)
        
        self.im.clear()
        
        self.im.setImage(
            self.spectrogram,
            rect=[0, 0, SPECTRO_HISTORY_SIZE, SAMPLING_RATE],
            autoLevels=False
        )
