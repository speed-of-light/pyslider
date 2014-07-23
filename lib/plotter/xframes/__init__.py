__all__ = []

import matplotlib.cm as mcm
from functools import wraps  # enables @wraps
from lib.plotter.plot_filer import _PlotFiler as PF
from roc_plot import _RocPlot as Rocp
from roc_grid import _RocGrid as Rgrid
from frames import _Frames as Frs
from mater import _Mater as Mater


class XframePlotter(PF):
    _cm = mcm.jet
    _markers = ["s", "o", "^", "D"]

    def __init__(self, xfe=None):
        self.xfe = xfe
        self.save_fig = True

    def __ds_key(self):
        return "[{}-{}]".format(self.xfe.root, self.xfe.name)

    def __rn(self, more=""):
        return self.xfe.root + "_" + self.xfe.name + more

    def __red_ary(self, ary):
        return reduce(lambda x,y: "{},{}".format(x, y), ary)

    def __plot_base(func):
        @wraps(func)  # enable func.__name__
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            more = "_s{}".format(kwargs["st"]) if "st" in kwargs else ""
            more += "_o{}".format(self.__red_ary(kwargs["obk"])) if "obk" in kwargs else ""
            PF._savefig(self, kwargs["fig"], func.__name__,
                        self.__rn(more=more))
            # return data
        return inner

    @__plot_base
    def roc_curve(self, fig=None):
        ax = fig.add_subplot(111)
        rop = Rocp(self.__ds_key(), self._cm, self._markers)
        data = self.xfe.roc_details(keys=range(4))
        rop.plot(ax, data)
        return data

    @__plot_base
    def roc_curve_plus(self, fig=None, data=None):
        if data is None:
            data = self.xfe.roc_details(keys=range(0, 18))
        rop = Rgrid(self.__ds_key(), self._cm)
        rop.plot(fig, data)

    @__plot_base
    def ns_frame_list(self, fig=None, data=None, st=0):
        pt = Frs(self.__ds_key(), self.xfe.root, self.xfe.name)
        pt.plot(fig, data, st=st)

    @__plot_base
    def dist_mat(self, fig=None, data=None, st=0, obk=[0,1]):
        """
        st: starting point of data
        obk: observing key
        """
        pt = Mater(self.__ds_key(), self.xfe.gnd.info().n_slides, obk)
        pt.plot(fig, data, st)
