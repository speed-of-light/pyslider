__all__ = ["core", "single_matching_plotter"]

from lib.exp.evaluator.ground_truth import GroundTruth as GT
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

    def slice_bar(self, ax, x, y, z, start, size, cmm):
        end = start+size
        gt = GT(self.root, self.name)
        for fi, mv, fid in zip(range(1, size+1), z[start: end], y[start:end]):
            cr = [cmm(fi*3./size)]*len(mv)
            asid = int(gt.answer(fid))
            fac = 1
            if asid > 0:
                print asid, fid
                cr[asid-1] = '#FF5698'
            else:
                cr = ['#aa77FF']*len(mv)
                mv = mv/max(mv)
                fac = max(mv)
            ax.bar(x, mv, fid, zdir='y', color=cr, alpha=0.4)
            mi = min(xrange(len(mv)), key=mv.__getitem__)
            ax.bar([x[mi]], [mv[mi]*fac/2.0], fid,
                   zdir='y', color=['#44FF32'], alpha=.8)
        ax.view_init(elev=60., azim=120)
