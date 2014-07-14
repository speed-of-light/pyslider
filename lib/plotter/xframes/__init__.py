import matplotlib.cm as mcm
from roc_plot import _RocPlot as Rocp


class XframePlotter(object):
    _cm = mcm.jet
    _markers = ["s", "o", "^", "D"]

    def __init__(self, xfe=None):
        self.xfe = xfe

    def __ds_key(self):
        return "[{}-{}]".format(self.xfe.root, self.xfe.name)

    def roc_curve(self, fig):
        ax = fig.add_subplot(111)
        rop = Rocp(self.__ds_key(), self._cm, self._markers)
        rop.plot(ax, self.xfe.evaluate(keys=range(4)))
