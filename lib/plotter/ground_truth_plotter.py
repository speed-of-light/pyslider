import matplotlib.cm as mcm
from base import Plotter
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
