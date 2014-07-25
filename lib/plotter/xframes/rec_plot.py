import numpy as np
from lib.plotter.ax_helper import AxHelper


class _RecPlot(object):
    def __init__(self, ks="", data=None):
        self.ks = ks
        self.df = data

    _atmri = dict(
            a="Area", at="Area and top50", atm="Area, top50, mean",
            atmri="Area, top50, mean, ransac, and inverse")

    def __translator(self, key):
        kegs = key.split("_")
        w = ""
        for keg in kegs:
            if keg == "v":
                continue
            elif keg in "atmri":
                rk = self._atmri[keg]
            elif keg in "ans":
                ak = "result"
            elif keg == "re":
                w = "with refine"
            else:
                w = "with customed weighting"
        return "{} {} {}".format(rk, w, ak)

    def __legends(self, ax, ax2):
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        leg = ax.legend(h1+h2, l1+l2, loc=8, ncol=6)
        leg.set_alpha(.6)

    def __title(self, ax, ks):
        tk = self.__translator(ks)
        ax.set_title(tk, fontsize=18)

    def __spine_info(self, ax, ax2):
        ax.patch.set_visible(False)
        ax.set_ylabel("Slide ID", fontsize=16)
        ax.set_xlabel("Candidate ID", fontsize=16)
        ax2.set_ylabel("Confidence", fontsize=16)
        ax2.set_ylim(0, 1)
        ax.set_xlim(0, max(self.df.index))

    def __base_plot(self, ax, ky):
        ax = self.df.plot(y=ky, legend=None, color='r', marker="^")
        ax = self.df.plot(y="gnd", legend=None, color='#88EF99', lw=2)
        ax2 = ax.twinx()
        self.df.plot(y=ky[:-4]+"_conf", ax=ax2, color="#88aeFc")
        return ax, ax2

    def __ploting(self, ax, ky):
        ax, ax2 = self.__base_plot(ax, ky)
        self.__spine_info(ax, ax2)
        self.__title(ax, ky)
        self.__legends(ax, ax2)

    def plot(self, fig, keys):
        oks = np.array(filter(lambda k: "ans" in k, self.df.columns))
        print "Keys available:", oks
        ks = oks[keys]
        fig.suptitle("Confidence VS Recognition results", fontsize=20, y=.93)
        for ki, ky in enumerate(ks, 1):
            ax = fig.add_subplot(len(keys)/2+1, 2, ki)
            self.__ploting(ax, ky)
