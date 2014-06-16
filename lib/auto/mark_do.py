from lib.exp.evaluator.ground_truth import GroundTruth as GT
from lib.plotter.matching.single_matching_plotter import \
    SingleMatchingPlotter as SMP


class MarkDo(object):
    def __init__(self, root, name):
        self.gt = GT(root, name)
        self.smp = SMP(root, name, None)
        self.df = self.gt.load("abs_pairs")
        print "Original length: {}".format(len(self.df))

    def add_mark(self, fig, sid, fid, preview=True):
        self.smp.set_matched_pair(sid, fid)
        view = self.smp.get_view()
        # show data
        if not preview:
            self.df = self.gt.add_mark(self.df, sid, fid, 1)
        print self.df[-5:]
        # plotting
        ax = fig.add_subplot(111)
        ax.imshow(view[:, :, [2, 1, 0]])

    def delete_mark(self, fid):
        """
        Delete mark by given `fid`
        """
        wi = self.df[self.df.fid == fid].index[0]
        self.df = self.df.drop(wi)

    def save_marks(self):
        """
        Save edited marks
        ** NOTICE: This can not be undo **
        """
        self.gt.save("abs_pairs", self.df)
