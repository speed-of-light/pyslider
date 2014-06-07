import matplotlib.cm as mcm
from base import Plotter
from ground_truth.segments import GtSegments


class GroundTruthPlotter(GtSegments):
    """
    Plot Ground truth segmented data
    """
    def __init__(self):
        """
        Here should put some plot configurations
        """
        cmap = mcm.Paired
        GtSegments.__init__(self, cmap)
        pass

    def plot(self):
        """
        Plot segments annotates
        """
        pass

