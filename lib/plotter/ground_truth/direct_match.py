from ..base import Plotter


class GtDirectMatch(Plotter):
    def __init__(self, **kwargs):
        Plotter.__init__(self, **kwargs)

    def __legend(self, ax, lns):
        labels = [l.get_label() for l in lns]
        ax.legend(lns, labels, loc=0)

    def absolute_pairs(self, ax, pairs, top):
        dy = [p for p in pairs.sid]
        dx = [p for p in pairs.fid]
        ln = ax.plot(dx, dy, marker='x', label='Slide id')
        bn = ax.axvline(top, 0, max(dy), color='b', ls='-.', label='bound')
        lns = ln + [bn]
        self.__legend(ax, lns)

    def relative_pairs(self, ax, pairs):
        dy = [p for p in pairs.sid]
        dx = range(len(dy))
        lns = ax.plot(dx, dy, marker='x', label="Slide id")
        ax.set_xlim(0, dx[-1])
        self.__legend(ax, lns)
