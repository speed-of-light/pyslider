from mpl_toolkits.mplot3d import axes3d, Axes3D
from lib.exp.featx import Featx
from lib.exp.match import MatchApp
from lib.exp.evaluator import GroundTruth
from lib.plotter.matching import MatchingPlotter as MaP


class MatchDo(object):
    def __init__(self, root, name):
        """
        Deprecated
        Provide a simple way to rundown
        """
        self.root = root
        self.name = name

    def __hide_w0611(self):
        """
        Prevent pyflakes W0611
        """
        ax = axes3d()
        ax = Axes3D()
        print str(ax)

    def get_feats(self):
        ft = Featx(self.root, self.name)
        sfx = ft.get_slide_feats()
        ffx = ft.get_frame_feats()
        return sfx, ffx

    def get_match(self):
        self.mapp = MatchApp(self.root, self.name)
        ms = self.mapp.knn_ms()
        return ms

    def plot_match(self, fig, start=0, size=10):
        if size > 50:
            print "size larger than 50 is not recommanded for this plotter"
            return None
        maplot = MaP(self.root, self.name)
        ax = fig.add_subplot(111, projection='3d')
        maplot.sf_dist_bar(ax, self.mapp, gnd, None, start, size)
