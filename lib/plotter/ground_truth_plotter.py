from base import Plotter


class GroundTruthPlotter(Plotter):
    """
    Plot Ground truth segmented data
    """
    def __init__(self, segments):
        self.seg = segments

    def plot(self, ax):
        """
        Plot segments annotates
        """
        pass

    def segmentize(ax, segments_list):
        """
        Add segmented plot for input ground truth data
        """
        matplotlib.cm.hsv.N = 100
        max_x_lim = 0
        for si, sg in enumerate(segments_list):
            segs = [(dd[0], dd[1]) for dd in sg]
            segv = [matplotlib.cm.Paired(dd[-1]/48.0) for dd in sg]
            ax.broken_barh(segs, (10*si+2, 6), facecolors=segv)
            max_x_lim = max(max_x_lim, (sg[-1][0]+sg[-1][1]))  # from last frame id plus duration
        # update global style
        ax.set_ylim(0, 10*len(segments_list))  # set y max by value of y
        ax.set_xlim(0, max_x_lim*1.01)
        return ax
