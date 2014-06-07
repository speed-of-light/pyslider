from ..base import Plotter
from ..base import SegLocator


class GtSegments(Plotter):
    def __init__(self, **kwargs):
        Plotter.__init__(self, **kwargs)

    def __ano_sid(self, ax, gnd, seg_locator, tag_at):
        """
        Add annotation to text with tag position
        """
        txt_pos = seg_locator.txt_pos(gnd, tag_at)
        data_pos = seg_locator.data_pos(gnd)
        arp = dict(arrowstyle="-")
        ax.annotate(gnd[2], xy=data_pos, xytext=txt_pos,
                    xycoords='data', textcoords='data',
                    horizontalalignment='center')

    def __ano_sids(self, ax, gnds, seg_locator):
        for gi, gnd in enumerate(gnds):
            self.__ano_sid(ax, gnd, seg_locator, .7)

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

    def __ano_imgs(self, ax, segments, segl):
        for sg in segments:
          imp = "{}/{:03d}.jpg".format(self.img_base, sg[2])
          pos = segl.data_pos(sg[:2])
          art = Plotter.image_box(self, imp, pos, pos, .10)
          ax.add_artist(art)

    def segmentize_ax(self, ax, segments, segid=0):
        """
        Add segmented plot for input ground truth data
        """
        segl = SegLocator(segid, height=self.seg_height)
        segs, segv = self.__seg_xy(segments)
        col = ax.broken_barh(segs, segl.yrange(), facecolors=segv, antialiased=True)
        if self.img_base is not None:
            self.__ano_imgs(ax, segments, segl)
        self.__ano_sids(ax, segments, segl)
        # from last frame id plus duration
        max_x_lim = max(0, (segments[-1][0]+segments[-1][1]))
        xlim = ax.get_xlim()
        ax.set_xlim(xlim[0]*.99, max_x_lim*1.01)
        return col

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
