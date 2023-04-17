import traceback
import numpy as np

import pyqtgraph as pg
from pyqtgraph.graphicsItems.ScatterPlotItem import name_list
from pyqtgraph.Qt import QtWidgets, QtGui, QtCore
from pyqtgraph.parametertree import interact, ParameterTree, Parameter
import random
import sys
import math
from rt_formant.panel import Wave, FFT, Cepstrum, Spectrogram, Formant

from rt_formant.sound import SoundStream

pg.mkQApp()

rng = np.random.default_rng(10)
random.seed(10)


class Plot:
    def __init__(self, stream):
        layout = pg.GraphicsLayoutWidget()

        self.plots = [
            Wave(layout.addPlot(row=0, col=0, title="wave")),
            FFT(layout.addPlot(row=1, col=0, title="fft")),
            Cepstrum(layout.addPlot(row=2, col=0, title="ceps")),
            Spectrogram(layout.addPlot(row=0, col=1, title="ceps")),
            Formant(layout.addPlot(row=1, col=1, title="formants")),
        ]
        tree = ParameterTree()
        tree.setMinimumWidth(150)

        textbox = Parameter.create(name="text", type="text", readonly=True)
        tree.addParameters(textbox)

        win = QtWidgets.QWidget()
        win.setLayout(lay := QtWidgets.QHBoxLayout())
        lay.addWidget(layout)
        # lay.addWidget(tree)

        self.fps = 50

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(int(1 / self.fps * 1000))

        self.win = win
        self.timer = timer
        self.t = 0
        self.stream = stream

    def run_app(self):
        self.win.show()
        QtGui.QGuiApplication.instance().exec()

    def update(self):
        stream_data = self.stream.get()
        for item in self.plots:
            item.update(stream_data)


def main():
    stream = SoundStream()
    Plot(stream).run_app()


if __name__ == "__main__":
    main()
