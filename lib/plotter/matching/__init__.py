__all__ = ["core", "single_matching_plotter"]

import matplotlib.cm as mcm
from core import MatchingPlotterBase


class MatchingPlotter(MatchingPlotterBase):
    def __init__(self, root, name):
        """
        Try to show one matching pairs
        use set_data to set matched results:
            array of `sid`, `fid`, `matches`
        """
        MatchingPlotterBase.__init__(self, root, name)

    def __match_info(self, ax, df=None, sid=-1, fid=0):
        self.set_matched_pair(sid, fid)
        view = self.get_view()
        ax.imshow(view[:, :, [2, 1, 0]])
        info = "S-{}, F-{}, df: {:5.2f}({})".\
            format(sid, fid, df.dist.mean(), len(df))
        ax.set_title(info)

    def result_grid(self, fig, row=4, col=4, from_=1):
        start = from_ - 1
        end = from_+(row*col) - 1
        for mi, mc in enumerate(self.df[start:end], 1):
            ax = fig.add_subplot(15, 4, mi)
            self.__match_info(ax, **mc)

    def frame_slides_relation(self, ax, matches, answer):
        """
        Print frame to slides relation by input function
        """
        x = [s["sid"] for s in matches]
        y = [s["df"].dist.mean() for s in matches]
        ax.plot(x, y)

    def slides_frames_similarity(self, sids, fids, sims):
        pass

    def sf_dist_bar(self, ax, match_app, psids, start, size):
        """
        Show 3d comparable bar chart for slide and frame similarity
        """
        x = match_app.slide_seeds()
        y = match_app.frame_seeds()
        z = match_app.knn_ms()
        for data in self.iter_slideset(x, y, z, psids, start, size):
            self.slideset_bar(ax, match_app.gnd, mcm.gray, x, **data)
        ax.view_init(elev=60., azim=120)
