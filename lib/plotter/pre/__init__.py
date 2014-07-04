__doc__ = """
Preprocessing data result plotter
"""

__all__ = []

from matplotlib.ticker import FuncFormatter
from lib.exp.evaluator.preproc_evaluator import PreprocEvaluator
from lib.exp.pre import Reducer


class PrePlotter(object):
    def __init__(self):
        rkeys = ["diff_next/size_2",
                 "diff_next/size_15",
                 "diff_next/size_30",
                 "diff_next/size_60",
                 "diff_next/size_300",
                 "diff_bkg"]
        mnames = ["Avg 2", "Avg 15", "Avg 30",
                  "Avg 60", "Avg 300", "Bkg Model"]
        self.rkeys = rkeys
        self.names = mnames

    def _frame_time_formatter(self, data, pos):
        sec = (data)/30
        return "{: 5.1f}".format(sec)

    def diff_plot(self, ax, data, hls):
        data.plot(ax=ax, label="Difference", c='g', marker='>')
        ah, al = ax.get_legend_handles_labels()
        mean = data.mean()
        ax.hlines(mean, 0, max(data.index), color='g')
        ax.set_ylabel("Frame Difference", fontsize=15)
        ax.set_xlabel("Candidate Index", fontsize=15)
        hls = self.__add__handles_labels(hls, ah, al)
        return ax, hls

    def dist_plot(self, ax, data, hls):
        ax = data.plot(ax=ax, label="Frame Distance", secondary_y=True, c='r',
                       marker='x')
        ah, al = ax.get_legend_handles_labels()
        ax.hlines(data.mean(), 0, max(data.index), color='r')
        ax.set_ylabel("Frame Delay (Seconds)", fontsize=15)
        ax.yaxis.set_major_formatter(FuncFormatter(self._frame_time_formatter))
        hls = self.__add__handles_labels(hls, ah, al)
        return ax, hls

    def __add__handles_labels(self, hl, newh, newl):
        if hl is None:
            hl = [newh, newl]
        else:
            hl[0] = hl[0] + newh
            hl[1] = hl[1] + newl
        return hl

    def fc_delay_relations(self, ax, data, cols,
                           key="Delay-time vs Frame Difference"):
        """
        data: dataframe with columns `diff`, `dist`
        """
        hls = None
        if "diff" in cols:
            ax, hls = self.diff_plot(ax, data["diff"], hls)
        if "dist" in cols:
            ax, hls = self.dist_plot(ax, data["dist"], hls)
        ax.set_xlim(0, max(data.index))
        ax.legend(hls[0], hls[1], loc=0)
        ax.set_title(key, fontsize=18, y=1.03)
        return ax

    def __get_reduced_data(self, re, rk, pp):
        prk = "/reduce/{}".format(rk)
        red = re.load(prk)
        scf = pp.ac_reduced_to_slides(red)
        return scf

    def batch_delay_relations(self, fig, root, name):
        """
        Usage:
            fig = plt.figure(figsize=(15, 38))
            ppt.batch_delay_relations(fig, *dn)
        """
        pp = PreprocEvaluator(root, name)
        re = Reducer(root, name)
        dzip = zip(range(len(self.names)), self.names, self.rkeys)
        for ri, na, rk in dzip:
            df = self.__get_reduced_data(re, rk, pp)
            # plot
            ax = fig.add_subplot(len(self.names), 1, ri)
            title = "[Data: {}-{}] {}".format(root, name, na)
            self.fc_delay_relations(ax, df, cols=["diff", "dist"], key=title)
