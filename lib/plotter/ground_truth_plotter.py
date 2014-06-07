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
    def __init__(self, segments):
        self.sg_list = segments

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

    def segmentize(self, ax, base=0):
        """
        Add segmented plot for input ground truth data
        """
        max_x_lim = 0
        min_x_lim = 9999999
        segl = SegLocator(height=10)
        sglist = self.sg_list
        for si, sg in enumerate(sglist):
          segs, segv = self.__seg_xy(sg)
          segl.nth = si + base
          ax.broken_barh(segs, segl.yrange(), facecolors=segv)
          self.__ano_sids(ax, sg, segl)
          # from last frame id plus duration
          max_x_lim = max(max_x_lim, (sg[-1][0]+sg[-1][1]))
          min_x_lim = min(min_x_lim, sg[-1][0])
        # update global style
        xlim = ax.get_xlim()
        ax.set_xlim(xlim[0], max_x_lim*1.01)
        return ax
