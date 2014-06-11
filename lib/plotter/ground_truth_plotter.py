import matplotlib.cm as mcm
from ground_truth.segments import GtSegments
from ground_truth.direct_match import GtDirectMatch


class GroundTruthPlotter(GtSegments, GtDirectMatch):
    """
    Plot Ground truth segmented data
    """
    def __init__(self):
        """
        Here should put some plot configurations
        """
        GtSegments.__init__(self, cmap=mcm.Paired)

    def group_pair(self, fig, kwargs):
        """
        kwargs:
            `gnd_raw`: raw ground truth data
            `info`: summary of each keys
        """
        ax = fig.add_subplot(111)
        lns = []
        for key in kwargs.keys():
            df = kwargs[key]['gnd_raw']
            top = kwargs[key]['info'].n_frames
            ln = self.absolute_pairs(ax, df[df.sid > 0], top, key)
            lns.append(ln[0])
        self.set_legends(ax, lns)
        self.set_titles(ax, "GroundTruth of Slide-Frame Pairs")
        return fig
