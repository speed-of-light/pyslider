__all__ = []

import matplotlib.cm as mcm
from functools import wraps  # enables @wraps
from lib.plotter.plot_filer import _PlotFiler as PF
from roc_plot import _RocPlot as Rocp


class XframePlotter(PF):
    _cm = mcm.jet
    _markers = ["s", "o", "^", "D"]

    def __init__(self, xfe=None):
        self.xfe = xfe
        self.save_fig = True

    def __ds_key(self):
        return "[{}-{}]".format(self.xfe.root, self.xfe.name)

    def __rn(self):
        return self.xfe.root + "_" + self.xfe.name

    def __plot_base(func):
        @wraps(func)  # enable func.__name__
        def inner(self, *args, **kwargs):
            data = func(self, *args, **kwargs)
            PF._savefig(self, kwargs["fig"], func.__name__, self.__rn())
            return data
        return inner

    @__plot_base
    def roc_curve(self, fig=None):
        ax = fig.add_subplot(111)
        rop = Rocp(self.__ds_key(), self._cm, self._markers)
        data = self.xfe.roc_details(keys=range(4))
        rop.plot(ax, data)
        return data
