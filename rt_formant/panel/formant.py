import pyqtgraph as pg
import numpy as np
from rt_formant.sound import BUFF_SIZE, SAMPLING_RATE
from rt_formant.signal import detect_peaks_raw, lifter

SPECTRO_HISTORY_SIZE = 60

class Formant:
    def __init__(self, plot_item: pg.PlotItem):
        self.plot_item = plot_item
        self.spectrogram = np.zeros(
            shape = (SPECTRO_HISTORY_SIZE, BUFF_SIZE)
        )
        cmap = pg.colormap.getFromMatplotlib("gray")
        self.im = pg.ImageItem(border="k", cmap=cmap)

        plot_item.addItem(self.im)
        self.plot_item.setYRange(0, SAMPLING_RATE / 8, padding = 0)
        self.plot_item.setXRange(0, SPECTRO_HISTORY_SIZE, padding = 0)
        plot_item.addColorBar( self.im, colorMap='gray', values=(0, 1) )

    def update(self, data):
        lifter_array = lifter(data)
        peak_of_lifter = detect_peaks_raw(lifter_array)
        
        result = np.zeros_like(data)
        for i in peak_of_lifter:
            result[i] = 1
        
        self.spectrogram[:-1, :] = self.spectrogram[1:, :]
        self.spectrogram[-1, :] = result
        
        self.im.clear()        
        self.im.setImage(
            self.spectrogram,
            rect=[0, 0, SPECTRO_HISTORY_SIZE, SAMPLING_RATE],
            autoLevels=False
        )
