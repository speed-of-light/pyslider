from ..exp.evaluator.ground_truth import GroundTruth


class Batcher(object):
    def __init__(self):
        """
        A class to run processes across multiple dataset
        """
        pass

    def __prog_report(self, root, name, data):
        print "-----", root, name, "-----"
        print data

    def setup_univ_gnd(self, roots, names):
        """
        Auto save/create univ type groundtruth data
        expected to see root, name, `abs_pairs`, `rel_paris`, `segments`
        """
        for (r, n) in zip(roots, names):
            gt = GroundTruth(r, n)
            df = gt.univ_df()
            gt.save("abs_pairs", df[df.sid > 0])
            gt.save("rel_pairs", gt.shrink(df[df.sid > 0]))
            gt.save("segments", gt.segments_df(df[df.sid > 0]))
            self.__prog_report(r, n, gt.load("keys"))

    def delete_ground_truth(self, roots, names):
        """
        Do a batched store deletion
        """
        for (r, n) in zip(roots, names):
            gt = GroundTruth(r, n)
            gt.delete_file()
            self.__prog_report(r, n, gt.load("keys"))
