from ..base import Plotter


class GtDirectMatch(Plotter):
    def __init__(self, **kwargs):
        Plotter.__init__(self, **kwargs)

    def set_markers(self, ax, handles):
        mks = Plotter.markers(self)
        ml = len(mks)
        for hi, h in enumerate(handles):
            mk = mks[hi % ml]
            h.set_marker(mk)

    def set_legends(self, ax, handles):
        """
        Use to add legends for axes plotted with multiple data set
        lhs: line handles of axes
        """
        labels = [h.get_label() for h in handles]
        ax.legend(handles, labels, loc=0)

    def __txy(self, ax, title, x, y):
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    def set_titles(self, ax, title="Slide - Frame pairs"):
        """
        Set x, y, labels and axes title
        """
        self.__txy(ax, title, "Frame", "Slide")

    def absolute_pairs(self, ax, pairs, xtop, name="Slide ID"):
        """
        Plot ground truth data with line-wise pairs
        top: the frame limit from a video
        name:
        """
        dy = [p for p in pairs.sid]
        dx = [p for p in pairs.fid]
        ln = ax.plot(dx, dy, marker='x', label=name)
        ax.axvline(xtop, 0, max(dy), color=ln[0].get_color(),
                   ls='-.', label='bound', lw=2)
        return ln

    def relative_pairs(self, ax, pairs, name="Slide ID"):
        dy = [p for p in pairs.sid]
        dx = range(1, len(dy)+1)
        oxlim = max(ax.get_xlim()[1], max(dx))
        ln = ax.plot(dx, dy, marker='x', label=name)
        ax.set_xlim(0, oxlim+1)
        return ln
