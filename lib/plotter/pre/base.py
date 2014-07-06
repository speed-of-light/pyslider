from matplotlib.ticker import FuncFormatter
from lib.exp.pre import Const


class _Base(object):
    def __init__(self):
        pass

    def _name_key_zip(self):
        inxs = range(len(Const.Names))
        iz = zip(inxs, Const.Names, Const.Rkeys, Const.Doffsets)
        return iz

    def __key_is_blank(self, key):
        sd = self.__dict__
        return (not hasattr(self, key)) or (sd[key] is None) or (sd[key] == "")

    def __rootname_not_set(self):
        return self.__key_is_blank("root") or \
            self.__key_is_blank("name")

    def _assert_rootname_exist(self):
        if self.__rootname_not_set():
            info = "set_rootname() before calling this function"
            print info
            raise Exception("Error", info)

    def _frame_time_formatter(self, data, pos):
        sec = (data)/30
        return "{: 5.1f}".format(sec)

    def set_rootname(self, root, name):
        self.root = root
        self.name = name
        self.rn = "{}_{}".format(root, name)
        self.rootname = "[Data: {}-{}]".format(root, name)

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

    def diff_plot(self, ax, data, hls):
        data.plot(ax=ax, label="Difference", c='g', marker='>')
        ah, al = ax.get_legend_handles_labels()
        mean = data.mean()
        ax.hlines(mean, 0, max(data.index), color='g')
        ax.set_ylabel("Frame Difference", fontsize=15)
        ax.set_xlabel("Candidate Index", fontsize=15)
        hls = self.__add_ser_lelabs(hls, ah, al)
        return ax, hls

    def dist_plot(self, ax, data, hls):
        ax = data.plot(ax=ax, label="Frame Distance", secondary_y=True, c='r',
                       marker='x')
        ah, al = ax.get_legend_handles_labels()
        ax.hlines(data.mean(), 0, max(data.index), color='r')
        ax.set_ylabel("Frame Delay (Seconds)", fontsize=15)
        ax.yaxis.set_major_formatter(FuncFormatter(self._frame_time_formatter))
        hls = self.__add_ser_lelabs(hls, ah, al)
        return ax, hls

    def _title_tag(self, info):
        title = "{} {}".format(self.rootname, info)
        return title

    def _shr_sc_cp_labs(self, ax):
        """
        Slide Hit Ratio, Slide Coverage ComParison Labels
        """
        hx, lx = ax.get_legend_handles_labels()
        lelabs = ["Segments Hit-ratio", "Slide Coverage"]
        ax.legend(hx, lelabs, loc='lower center', ncol=3,
                  fancybox=False, shadow=True, fontsize=14)
        ax.set_xlabel("Methods", fontsize=15)
        ax.set_xticklabels(Const.Names, fontsize=15, rotation=0)
        ax.set_ylabel("Percentage(%)", fontsize=15)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda v, p: "{:3.1f}".format(v*100)))
        title = self._title_tag("Segments and slide soverage")
        ax.set_title(title, y=1.02, fontsize=18)

    def _shr_sc_texts(self, ax, data):
        for pdi, pd in data.iterrows():
            shrf = "{:3.2f}".format(pd.segments_hit_ratio*100)
            ax.text(pdi+0.3, pd.segments_hit_ratio, shrf,
                    va='bottom', fontsize=12)
            scf = "{:3.2f}".format(pd.slide_coverage*100)
            ax.text(pdi+0.7, pd.slide_coverage, scf, va='bottom', fontsize=12)

    def _common_axes(self, fig):
        ax = fig.add_subplot(111)
        ax.patch.set_alpha(.0)
        return ax
