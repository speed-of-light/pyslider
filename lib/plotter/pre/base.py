from matplotlib.ticker import FuncFormatter


class _Base(object):
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

    def __add__handles_labels(self, hl, newh, newl):
        if hl is None:
            hl = [newh, newl]
        else:
            hl[0] = hl[0] + newh
            hl[1] = hl[1] + newl
        return hl

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

