from matplotlib.ticker import FuncFormatter
from lib.exp.pre import Const


class _CovPlot(object):
    def __init__(self, tag):
        self.tag = tag

    def __add_title(self, ax):
        name = "Segments and slide soverage"
        title = "{} {}".format(self.tag, name)
        ax.set_title(title, y=1.02, fontsize=18)

    def __add_legend(self, ax):
        lelabs = ["Segments Hit-ratio", "Slide Coverage"]
        hx, lx = ax.get_legend_handles_labels()
        leg = ax.legend(hx, lelabs, loc='lower center', ncol=3,
                  fancybox=False, shadow=True, fontsize=14)
        leg.get_frame().set_alpha(0.8)

    def __add_labels(self, ax):
        ax.set_xlabel("Methods", fontsize=15)
        ax.set_xticklabels(Const.Names, fontsize=15, rotation=0)
        ax.set_ylabel("Percentage(%)", fontsize=15)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda v, p: "{:3.1f}".format(v*100)))

    def __add_texts(self, ax, data):
        for pdi, pd in data.iterrows():
            shrf = "{:3.2f}".format(pd.segments_hit_ratio*100)
            ax.text(pdi+0.3, pd.segments_hit_ratio, shrf,
                    va='bottom', fontsize=12)
            scf = "{:3.2f}".format(pd.slide_coverage*100)
            ax.text(pdi+0.7, pd.slide_coverage, scf, va='bottom', fontsize=12)

    def plot(self, ax, data):
        data.plot(kind='bar', ax=ax)
        self.__add_labels(ax)
        self.__add_legend(ax)
        self.__add_title(ax)
        self.__add_texts(ax, data)
