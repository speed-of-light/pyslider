from matplotlib.ticker import FuncFormatter
from lib.exp.pre import Const
from lib.plotter.ax_helper import AxHelper


class _DelayPlot(AxHelper):
    def __init__(self, data):
        self.data = data

    def __frame_time_formatter(self, data, pos):
        """
        TODO move to common
        """
        sec = (data)/30
        return "{: 5.1f}".format(sec)

    def __fig_conf(self, ax, ah, al, xmax, key=""):
        ax.set_xlim(0, xmax)
        leg = ax.legend(ah, al, loc=0)
        leg.get_frame().set_alpha(0.5)
        ax.set_title(key, fontsize=18, y=1.03)

    def __add_ser_lelabs(self, hl, newh, newl):
        """
        Add SERies LEgend LABleS
        """
        if hl is None:
            hl = [newh, newl]
        else:
            hl[0] = hl[0] + newh
            hl[1] = hl[1] + newl
        return hl

    def __diff_plot(self, ax, data, hls):
        ax = data.plot(ax=ax, label="Difference", c='g', marker='>')
        ah, al = ax.get_legend_handles_labels()
        mean = data.mean()
        ax.hlines(mean, 0, max(data.index), color='g')
        ax.set_ylabel("Frame Difference", fontsize=15)
        hls = self.__add_ser_lelabs(hls, ah, al)
        return hls

    def __dist_plot(self, ax, data, hls):
        ax = data.plot(ax=ax, label="Frame Distance", secondary_y=True, c='r',
                  marker='x')
        ah, al = ax.get_legend_handles_labels()
        ax.hlines(data.mean(), 0, max(data.index), color='r')
        ax.set_ylabel("Frame Delay (Sec)", fontsize=15)
        ax.yaxis.set_major_formatter(FuncFormatter(self.__frame_time_formatter))
        hls = self.__add_ser_lelabs(hls, ah, al)
        return hls

    def plot(self, fig, rn=""):
        self._ax_hide_patch_spine_axis(fig.axes[0])
        ot = "Candidates Delay Time(ms)"
        fig.suptitle("{} {}".format(rn, ot), fontsize=20, y=.98)
        for di, dt in enumerate(self.data, 1):
            ax = fig.add_subplot(len(self.data), 1, di)
            ax.patch.set_alpha(0.0)
            data = dt["df"]
            hls = self.__dist_plot(ax, data["dist"], None)
            hls = self.__diff_plot(ax, data["diff"], hls)
            self.__fig_conf(ax, hls[0], hls[1], max(data.index), dt["key"])
        ax.set_xlabel("Candidate Index", fontsize=15)
