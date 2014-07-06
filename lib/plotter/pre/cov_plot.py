from matplotlib.ticker import FuncFormatter
from lib.plotter.ax_helper import AxHelper


class _CovPlot(AxHelper):
    def __init__(self, tag):
        AxHelper.__init__(self)
        self.tag = tag

    def __title(self, ax):
        name = "Segments and slide soverage"
        title = "{} {}".format(self.tag, name)
        ax.set_title(title, y=1.02, fontsize=18)

    def __legend(self, ax):
        lelabs = ["Segments Hit-ratio", "Slide Coverage"]
        hx, lx = ax.get_legend_handles_labels()
        leg = ax.legend(
            hx, lelabs, loc='lower center', ncol=3,
            fancybox=False, shadow=True, fontsize=14)
        leg.get_frame().set_alpha(0.8)

    def __labels(self, ax, xlabs):
        ax.set_xlabel("Methods", fontsize=15)
        ax.set_xticklabels(xlabs, fontsize=15, rotation=0)
        ax.set_ylabel("Percentage(%)", fontsize=15)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda v, p: "{:3.1f}".format(v*100)))

    def __top_ratio(self, ax, data):
        for pdi, pd in data.iterrows():
            shrf = "{:3.2f}".format(pd.segments_hit_ratio*100)
            ax.text(pdi+0.3, pd.segments_hit_ratio, shrf,
                    va='bottom', fontsize=12)
            scf = "{:3.2f}".format(pd.slide_coverage*100)
            ax.text(pdi+0.7, pd.slide_coverage, scf, va='bottom', fontsize=12)

    def __point_base(self, ax, x, y, title, style="ro", ymax=1):
        ah = ax.plot(x, y, style, alpha=0)
        ax.set_ylim(0, ymax)
        ax.set_ylabel(title, fontsize=14)
        for zx, zy in zip(x, y):
            ax.text(zx, zy/2, zy, ha="center", va="bottom", fontsize=20)

    def __point_seg_hits(self, ax, data, shift=.4):
        ax2 = ax.twinx()
        x = data.index+.45
        y = data.segment_hits
        self.__point_base(ax2, x, y, "Segment Hits", "g>",
                          data.gnd_segments.max())

    def __point_slide_count(self, ax, data, shift=.8):
        ax2 = ax.twinx()
        self._ax_shift_yaxis(ax2, delta=1.05)
        x = data.index+.8
        y = data.slide_count
        self.__point_base(ax2, x, y, "Slide Count", "g>",
                          data.total_slides.max())

    def __base_common(self, ax, data):
        self.__labels(ax, data.method)
        self.__legend(ax)
        self.__title(ax)

    def plot(self, ax, data):
        cols = ["segments_hit_ratio", "slide_coverage"]
        data[cols].plot(kind='bar', ax=ax)
        self.__base_common(ax, data)
        self.__top_ratio(ax, data)
        self.__point_seg_hits(ax, data)
        self.__point_slide_count(ax, data)
        ax.set_xlim(0, len(data)+.25)
