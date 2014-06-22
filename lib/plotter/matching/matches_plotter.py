from lib.plotter.base import Plotter
from single_matching_plotter import SingleMatchingPlotter


class MatchesPlotter(Plotter):
    def __init__(self):
        """
        Matches plotter
        """
        pass

    def __plot_with_title(self, ax ,img, ci=None, sid=None, fid=None, ans=None):
        ax.imshow(img[:, :, [2, 1, 0]])
        ax.set_title("#{}: s{}-f{}, a[{}]".format(ci, sid, fid, ans))

    def check_pair(self, matchx, sid=None, fid=None, ans=None, ci=None):
        """
        Show slide frame pair for check use
        """
        data = None
        ltyps = []
        if sid > 0:
          matchx.pair_matches(sid, fid)
          data = dict(matches=matchx.matches[0]["df"])
          ltyps = ['_lines', '_position']
        smp = SingleMatchingPlotter(
            matchx.root, matchx.name, data, sid=sid, fid=fid)
        mview = smp.layering(ltyps)
        return mview

    def wrong_pairs(self, fig, matchx, wrongs):
        for wi, wrong in enumerate(wrongs, 1):
            ax = fig.add_subplot(len(wrongs)/4 + 1, 4, wi)
            mview = self.check_pair(matchx, **wrong)
            self.__plot_with_title(ax, mview, **wrong)
