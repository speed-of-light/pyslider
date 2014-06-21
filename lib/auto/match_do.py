import numpy as np
from lib.exp.base import ExpCommon
from lib.exp.prepare import Prepare
from lib.exp.matching import Matcher
from lib.exp.evaluator.ground_truth import GroundTruth
from lib.exp.evaluator.pair_evaluator import PairEvaluator


class MatchDo(ExpCommon):
    def __init__(self, root, name):
        """
        Deprecated
        Provide a simple way to rundown
        """
        self.root = root
        self.name = name
        ExpCommon.__init__(self, root, name)
        self.elog.info("Doer: init")

    def reduced_frames(self):
        """ Get preprocessed frames """
        pp = Prepare(self.root, self.name)
        df = pp.load("keys")
        pk = df[df.key.str.contains('reduce')].key.values[5]
        fids = pp.load(pk).frame_id.values.astype(np.int32)
        self.elog.info("Doer: reduced frames")
        return fids

    def gnd_mpairs(self):
        """
        load ground truth matched pairs
        TODO change univ_df() to pairs()
        """
        gt = GroundTruth(self.root, self.name)
        df = gt.univ_df()
        self.elog.info("Doer: gnd mpairs")
        return df

    def matching(self, fids, thres):
        mm = Matcher(self.root, self.name)
        res, sfs, vfs = mm.set_match(fids, ransac=False, thres=0.9)
        self.elog.info("Doer: matching")
        return res, sfs, vfs

    def evaluation(self, res, gnd):
        pe = PairEvaluator(res, gnd)
        er = pe.pairing()
        praf = pe.hitd_praf(er)
        self.elog.info("Doer: evaluation")
        return praf

    def rundown(self):
        fids = self.reduced_frames()
        # gnd = self.gnd_mpairs()
        res, sfs, vfs = self.matching(fids, .9)
        # praf = self.evaluation(res, gnd)
        return res, sfs, vfs
