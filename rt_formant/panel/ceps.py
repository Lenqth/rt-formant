import pyqtgraph as pg

from rt_formant.signal import detect_peaks, lifter, xgraph

class Cepstrum:
    def __init__(self, plot_item: pg.PlotItem):
        self.plot_item = plot_item

    def update(self, data):
        lifter_array = lifter(data)
        peak_of_lifter = detect_peaks(lifter_array)

        y = [lifter_array]
        self.plot_item.clear()
        self.plot_item.setLogMode(False, True)
        self.plot_item.setXRange(0, 8000, padding = 0)
        self.plot_item.setYRange(-6, 0, padding = 0)
        self.plot_item.multiDataPlot(x=xgraph, y=y, pen=["lightgreen", "darkblue", "white"])
        self.plot_item.plot(x=peak_of_lifter, y=[1 for i in range(len(peak_of_lifter))], pen=None, symbol="o", symbolBrush="white" )
