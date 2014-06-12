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

    def __make_handle(self, ax, data, key, target):
        df = data[target]
        dio = data["info"]
        if target == "absp":
            top = dio.n_frames
            ln = self.absolute_pairs(ax, df, top, key)
        elif target == "relp":
            ln = self.relative_pairs(ax, df, key)
        return ln[0]

    def group_pair(self, fig, kwargs, target):
        """
        `target`: data in kwargs ready to be plot
        kwargs:
            `gnd_raw`: raw ground truth data
            `info`: summary of each keys
        """
        ax = fig.add_subplot(111)
        lns = []
        for key in kwargs.keys():
            lns.append(self.__make_handle(ax, kwargs[key], key, target))
        GtDirectMatch.set_markers(self, ax, lns)
        GtDirectMatch.set_legends(self, ax, lns)
        GtDirectMatch.set_titles(self, ax, "GroundTruth of Slide-Frame Pairs")
        return fig
