from ..base import Plotter
from ..base import SegLocator


class GtSegments(Plotter):
    def __init__(self, cmap):
        Plotter.__init__(self)
        self.cmap = cmap
        self.seg_height = 10

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
            self.__ano_sid(ax, gnd, seg_locator, (gi % 3+1)*.05 + .55)

    def __seg_xy(self, segl):
        segs = [(dd[0], dd[1]) for dd in segl]
        segv = [dd[-1] for dd in segl]
        msv = max(segv)
        segc = [self.cmap(cc*1.0/msv) for cc in segv]
        return segs, segc

    def __set_ax_ymax(self, ax, max_):
        ax.set_ylim(0, max_)

    def __new_layer(self, ax, aid, ymax):
        # hide what should hide
        ax.patch.set_visible(False)
        ax.yaxis.set_visible(False)
        for spinename, spine in ax.spines.iteritems():
            if spinename != 'bottom':
                spine.set_visible(False)
        # move new xaxis down
        ax.spines['bottom'].set_position(('data', self.seg_height*aid))
        self.__set_ax_ymax(ax, ymax)

    def segmentize_ax(self, ax, segments, segid=0):
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
        ax.set_xlim(xlim[0]*.99, max_x_lim*1.01)
        return ax

    def segmentize_fig(self, fig, segments_list):
        ax = fig.add_subplot(111)
        ymax = len(segments_list)*self.seg_height
        self.__set_ax_ymax(ax, ymax)
        for si, sg in enumerate(segments_list):
            if si > 0:
                ax = fig.add_axes(ax.get_position())
                self.__new_layer(ax, si, ymax)
            self.segmentize_ax(ax, sg, si)

    def even_segments(self, fig, segments):
        """
        Get evenly splitted segments on plot
        """
        cs = Plotter.chunks(self, segments, 10)
        self.segmentize_fig(fig, list(cs))
