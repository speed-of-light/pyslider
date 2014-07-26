from functools import wraps  # enables @wraps
from lib.plotter.plot_filer import _PlotFiler as PF
from lib.exp.summ import Mary
from fig_plot import FigPlot


class MaryPlotter(PF):
    def __init__(self):
        # Summ-Mary plotter
        PF.__init__(self)
        self.save_fig = True
        self.mm = Mary()

    def save_fig(func):
        @wraps(func)  # enable func.__name__
        def inner(self, *args, **kwargs):
            data = func(self, *args, **kwargs)
            kss = reduce(lambda x, y: "{},{}".format(x, y), kwargs["ks"])
            PF._savefig(self, kwargs["fig"], func.__name__,
                        "summary_{}".format(kss))
            return data
        return inner

    @save_fig
    def classfy_perf(self, fig=None, ks=[]):
        dc = self.mm.df_classify_perf()
        pt = FigPlot(dc)
        pt._classfy_roc(fig, ks)
