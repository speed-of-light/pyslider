from lib.exp.tools.video import Video
from lib.plotter.ax_helper import AxHelper


class _Frames(AxHelper):
    def __init__(self, keyname, root, name):
        self.kn = keyname
        self.vid = Video(root, name)

    def __recolor_spine(self, ax, pos="top", color="r"):
        if color is not None:
            ax.spines[pos].set_color(color)

    def __bold_axes(self, ax, xM=0, yM=0, c="r", lw=5):
        ax.axvline(color=c, lw=lw)
        ax.axvline(x=xM, color=c, lw=lw)
        ax.axhline(color=c, lw=lw)
        ax.axhline(y=yM, color=c, lw=lw)

    def __recolor_ax_spine(self, ax, c="r"):
        rca = lambda pos, clr: self.__recolor_spine(ax, pos, clr)
        map(rca, ["top", "right", "bottom", "left"], [c]*4)

    def __remake_spines(self, ax, isize, c="r"):
        self.__recolor_ax_spine(ax, c=c)
        self.__bold_axes(ax, xM=isize[1], yM=isize[0], c=c)

    def __plot_frame(self, ax, fimg):
        ax.imshow(fimg[:, :, [2, 1, 0]])
        self._ax_hide_ticks(ax)

    def __ax_annotates(self, ax, isize, sid, ans, fid):
        ax.set_title("S[{}]".format(int(sid)))
        ax.set_xlabel("A[{}]F[{}]".format(int(ans), int(fid)))
        if (sid > 0) & (ans == 0):
            self.__remake_spines(ax, isize, c="#77FF88")
        elif (sid <= 0) & (ans == 0):
            self.__remake_spines(ax, isize, c="r")

    def __prep_data(self, fig, df, st, se, ansk):
        fts = "Classified Frames of {} ({}~{})".format("Univ_07-coates", st, se)
        fig.suptitle(fts, fontsize=18, y=.93)
        daf = df[df[ansk] == 0][st:se]
        return daf

    def __fpa(self, fig, fid, rows, cols, index):
        # frame per ax
        vd = self.vid.get_frames([fid]).next()
        ax = fig.add_subplot(rows, cols, index)
        self.__plot_frame(ax, vd["img"])
        return ax, vd["img"]

    def plot(self, fig=None, df=None, key="bot_area", st=0):
        """
        key: column prefix in df, contained key_ans, key_gnd for
            color true positive and false positive results.
        st: start index of all slide candidates in df
        """
        cols, rows = 10, 7
        ansk = "{}_ans".format(key)
        daf = self.__prep_data(fig, df, st, st+cols*rows, ansk)
        for di, df in daf.iterrows():
            ax, img = self.__fpa(fig, df.fid, rows, cols, len(fig.axes)+1)
            self.__ax_annotates(ax, img.shape,
                                df["{}_gnd".format(key)], df[ansk], df.fid)

    def splot(self, fig=None, df=None, key="bot_area", st=0):
        """
        key: column prefix in df, contained key_ans, key_gnd for
            color true positive and false positive results.
        st: start index of all slide candidates in df
        """
        cols, rows = 10, 7
        ansk = "{}_ans".format(key)
        for di, dr in df.iterrows():
            if len(fig.axes) == rows*cols:
                break
            ax, img = self.__fpa(fig, dr.fid, rows, cols, len(fig.axes)+1)
            self.__ax_annotates(ax, img.shape, dr.gnd, dr[ansk], dr.fid)
