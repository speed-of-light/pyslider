from matplotlib.ticker import FuncFormatter
import matplotlib.cm as mcm
import numpy as np
from lib.exp.pre import Const


class _RtPlot(object):
    def __init__(self, reducer):
        self.re_ = reducer
        pass

    def __load_reduced_rtdf(self):
        rdf = self.re_.load("rtlog")
        rdf["left"] = rdf.origin - rdf.thresed - rdf.final
        return rdf

    def __bar_kwa(self, cm, y="origin", ha="//"):
        cr = np.array(cm)
        ma = [0.09, .2, .05, 0.3]
        kb = 'bar'
        st = True
        kwa = dict(y=y, kind=kb, stacked=st, hatch=ha, ec=cr-ma, color=cr)
        return kwa

    def __base_bar(self, ax, data):
        """
        Plot stacked bar chart with `origin`, `thresed`, `final` data
        """
        kwa = self.__bar_kwa(mcm.Paired(.6), y="origin")
        data.plot(ax=ax, **kwa)
        kwa = self.__bar_kwa(mcm.Paired(.3), y="thresed", ha="x")
        data.plot(ax=ax, **kwa)
        kwa = self.__bar_kwa(mcm.Paired(.1), y="final", ha="o")
        data.plot(ax=ax, **kwa)

    def __line_ratio_texts(self, ax, data):
        for pdi, pd in data.iterrows():
            pfr = pd.final*1./pd.origin
            ax.text(pdi-.5, pfr*.93, "{:5.2f}%".format(pfr*100), ha='center',
                    va='bottom', color='b', fontsize=12)

    def __line_frame_ratio(self, ax, data):
        ax2 = ax.twinx()
        rat = data.final*1./data.origin
        ax2.plot(data.index+(-.5), rat, '--ro', label="Reduced Rate")
        ax2.set_ylabel("Frames Ratio(%)", fontsize=15)
        ax2.set_yticklabels(ax2.get_yticklabels(), fontsize=13)
        fmt = FuncFormatter(lambda v, p: "{:3.2f}".format(v*100))
        ax2.yaxis.set_major_formatter(fmt)
        self.__line_ratio_texts(ax2, data)
        ah2, al2 = ax2.get_legend_handles_labels()
        return ah2, al2

    def __add_labs(self, ax, ah2, al2, data):
        ax.set_xticklabels(Const.Names, fontsize=15, rotation=0)
        hx, lx = ax.get_legend_handles_labels()
        labs = ["Origin", "Thresed", "Final"] + al2
        ax.legend(hx+ah2, labs, loc='upper center',
                  bbox_to_anchor=(0.5, 1),
                  ncol=5, fancybox=True, shadow=True, fontsize=14)
        ax.set_xlabel("Methods", fontsize=15)
        ax.set_ylabel("Frame Count", fontsize=15)
        ax.set_title("Frame reduced ratio", fontsize=20)
        ax.set_xlim(0, len(data))

    def __add_text(self, ax, pdi, pdy, pdv):
        x = pdi - .5
        t = "{: 5d}".format(pdv)
        ax.text(x, pdy, t, ha='center', fontsize=12)

    def __add_texts(self, ax, data):
        for pdi, pd in data.iterrows():
            pfr = pd.left/2+pd.thresed+pd.final
            self.__add_text(ax, pdi, pfr, int(pd.left))
            self.__add_text(ax, pdi, pd.thresed/2+pd.final, int(pd.thresed))
            self.__add_text(ax, pdi, pd.final/2, int(pd.final))

    def frame_reduced_ratio(self, ax):
        data = self.__load_reduced_rtdf()
        self.__base_bar(ax, data)
        ah2, al2 = self.__line_frame_ratio(ax, data)
        self.__add_labs(ax, ah2, al2, data)
        self.__add_texts(ax, data)
