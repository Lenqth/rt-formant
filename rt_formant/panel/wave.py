import pyqtgraph as pg


class Wave:
    def __init__(self, plot_item: pg.PlotItem):
        self.plot_item = plot_item

    def update(self, data):
        y = [data]
        self.plot_item.clear()
        self.plot_item.setXRange(0, len(data), padding = 0)
        self.plot_item.setYRange(-1, 1, padding = 0)
        self.plot_item.multiDataPlot(y=y, pen="red")
