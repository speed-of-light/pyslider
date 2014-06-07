from ..base import Plotter


class GtDirectMatch(Plotter):
    def __init__(self, **kwargs):
        Plotter.__init__(self, **kwargs)

    def __legend(self, ax, lns):
        labels = [l.get_label() for l in lns]
        ax.legend(lns, labels, loc=0)

    def __txy(self, ax, title, x, y):
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)

    def absolute_pairs(self, ax, pairs, top, name="Slide ID"):
        dy = [p for p in pairs.sid]
        dx = [p for p in pairs.fid]
        ln = ax.plot(dx, dy, marker='x', label=name)
        ax.axvline(top, 0, max(dy), color='b', ls='-.', label='bound')
        lns = ln
        self.__legend(ax, lns)
        self.__txy(ax, "GroundTruth of Slide-Frame pairs", "Frame", "Slide")

    def relative_pairs(self, ax, pairs, name="Slide ID"):
        dy = [p for p in pairs.sid]
        dx = range(len(dy))
        lns = ax.plot(dx, dy, marker='x', label=name)
        ax.set_xlim(0, dx[-1])
        self.__legend(ax, lns)
        self.__txy(ax, "GroundTruth of relative Slide-Frame pairs", "Time order", "Slide")
