__doc__ = """
Preprocessing data result plotter
"""

__all__ = []

from matplotlib.ticker import FuncFormatter


class PrePlotter(object):
    def __init__(self):
        pass

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

    def frame_candidates_relationships(self, ax, data, cols,
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
