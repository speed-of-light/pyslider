import numpy as np
from lib.exp.tools.video import Video


class _FramesPlot(object):
    def __init__(self, root, name):
        self.video = Video(root, name)

    def __get_all_frames(self, data, flag):
        if flag:
            flags = [True]*len(data)
        else:
            flags = data.sid > 0
        return data[flags]

    def __rand_list(self, data, flag, lim=50):
        rseeds = []
        if flag:
            ld = len(data)
            rlim = lim if lim < ld else ld
            rseeds = np.random.randint(1, len(data), rlim)
        else:
            rseeds = range(0, lim)
        return rseeds

    def set_data(self, data, **filters):
        df = self.__get_all_frames(data, filters["all_seg"])
        llim = filters["lim"] - len(filters["seeds"])
        rseeds = self.__rand_list(df, filters["rand"], llim)
        seeds = np.append(rseeds, filters["seeds"])
        seeds.sort()
        self.data = df.iloc[seeds.astype(np.int32)]

    def __atitle(self, ax, inx, fid, sid):
        ax.set_title("{}.{}[{}]".format(inx, fid, sid))
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)

    def make_patch_spines_invisible(self, ax):
        # TODO: Move to common package
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        for sp in ax.spines.itervalues():
            sp.set_visible(False)

    def plot(self, fig):
        self.make_patch_spines_invisible(fig.axes[0])
        for fi, (di, dv) in enumerate(self.data.iterrows(), 1):
            vd = self.video.get_frames([dv.fid]).next()
            ax = fig.add_subplot(6, 9, fi)
            ax.imshow(vd["img"][:, :, [2, 1, 0]])
            self.__atitle(ax, di, int(dv.fid), int(dv.sid))
            print "[", fi, dv.fid, "]",
        fig.suptitle("Random Selected Candidate Frames", fontsize=18, y=.95)
