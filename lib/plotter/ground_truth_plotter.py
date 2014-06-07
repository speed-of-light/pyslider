import matplotlib.cm as mcm
from base import Plotter


class SegLocator(object):
    def __init__(self, nth=0, height=10):
        """
        Get segment location information by given segment index and height
        """
        self.set_height(height)
        self.nth = nth

    def set_height(self, height):
        self.height = height
        self.__tag_at = height * 0.1
        self.__margin = height * 0.2
        self.__center = height * 0.5
        self.__content = height * 0.6

    def __brah_center(self, start, size):
        return start + size/2.0

    def __nth_base(self):
        """
        Return nth element of y-axis base position
        """
        return self.height * self.nth

    def yrange(self):
        """
        Return the range of y, start from (seg height)*si + content height,
            with height 6
        """
        return (self.__nth_base() + self.__margin,
                self.__content)

    def txt_pos(self, xinfo, tag_at=None):
        """
        xinfo: containing `start` and `size`, here use to get brah center
        """
        if tag_at is None:
            tag_at = self.__tag_at
        return (self.__brah_center(xinfo[0], xinfo[1]),
                self.__nth_base() + tag_at)

    def data_pos(self, xinfo):
        """
        xinfo: containing `start` and `size`, here use to get brah center
        """
        return (self.__brah_center(xinfo[0], xinfo[1]),
                self.__nth_base() + self.__center)


class GroundTruthPlotter(Plotter):
    """
    Plot Ground truth segmented data
    """
    def __init__(self):
        """
        Here should put some plot configurations
        """
        self.seg_height = 10
        pass

    def plot(self, ax):
        """
        Plot segments annotates
        """
        pass

    def __ano_sid(self, ax, gnd, seg_locator, tag_at):
        """
        Add annotation to text with tag position
        """
        txt_pos = seg_locator.txt_pos(gnd, tag_at)
        data_pos = seg_locator.data_pos(gnd)
        arp = dict(facecolor=(.5, .9, .5), shrink=0.05)
        ax.annotate(gnd[2], xy=data_pos, xytext=txt_pos,
                    xycoords='data', textcoords='data',
                    horizontalalignment='center',
                    arrowprops=arp)

    def __ano_sids(self, ax, gnds, seg_locator):
        for gi, gnd in enumerate(gnds):
            self.__ano_sid(ax, gnd, seg_locator, (gi % 3+1)*0.5)

    def __seg_xy(self, segl):
        mcm.Paired.N = 100
        segs = [(dd[0], dd[1]) for dd in segl]
        segv = [dd[-1] for dd in segl]
        msv = max(segv)
        segc = [mcm.Paired(cc*1.0/msv) for cc in segv]
        return segs, segc

    def segmentize(self, ax, segments, segid=0):
        """
        Add segmented plot for input ground truth data
        """
        max_x_lim = 0
        segl = SegLocator(segid, height=self.seg_height)
        segs, segv = self.__seg_xy(segments)
        ax.broken_barh(segs, segl.yrange(), facecolors=segv)
        self.__ano_sids(ax, segments, segl)
        # from last frame id plus duration
        max_x_lim = max(max_x_lim, (segments[-1][0]+segments[-1][1]))
        xlim = ax.get_xlim()
        ax.set_xlim(xlim[0], max_x_lim*1.01)
        return ax

    def __set_ax_ymax(self, ax, max_):
        ax.set_ylim(0, max_)

    def __new_layer(self, ax, aid):
        # hide what should hide
        ax.patch.set_visible(False)
        ax.yaxis.set_visible(False)
        for spinename, spine in ax.spines.iteritems():
            if spinename != 'bottom':
                spine.set_visible(False)
        # move new xaxis down
        ax.spines['bottom'].set_position(('outward', 15*aid))
        self.__set_ax_ymax(ax, ymax)

    def segmentize_fig(self, fig, segments_list):
        ax = fig.add_subplot(111)
        ymax = len(segments_list)*self.seg_height
        self.__set_ax_ymax(ax, ymax)
        for si, sg in enumerate(segments_list):
            if si > 0:
                ax = fig.add_axes(ax.get_position())
                self.__new_layer(ax, si)
            self.segmentize_ax(ax, sg, si)
