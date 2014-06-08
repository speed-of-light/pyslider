import numpy as np
from base import ExpCommon
from prepare import Prepare
from matching import Matcher
from evaluator.ground_truth import GroundTruth
from evaluator.pair_evaluator import PairEvaluator


class Doer(ExpCommon):
    """
    Provide a simple way to rundown
    """
    def __init__(self, root, name):
        self.root = root
        self.name = name
        ExpCommon.__init__(self, root, name)
        self.elog.info("Doer: init")

    def __reduced_frames(self):
        """ Get preprocessed frames """
        pp = Prepare(self.root, self.name)
        df = pp.load('keys')
        pk = df[df.key.str.contains('reduce')].key.values[5]
        fids = pp.load(pk).frame_id.values.astype(np.int32)
        self.elog.info("Doer: reduced frames")
        return fids

    def __gnd_mpairs(self):
        """
        load ground truth matched pairs
        TODO change univ_df() to pairs()
        """
        gt = GroundTruth(self.root, self.name)
        df = gt.univ_df()
        self.elog.info("Doer: gnd mpairs")
        return df

    def __matching(self, fids, thres):
        mm = Matcher(self.root, self.name)
        res, sfs, vfs = mm.set_match(fids, ransac=False, thres=0.9)
        self.elog.info("Doer: matching")
        return res

    def __evaluation(self, res, gnd):
        pe = PairEvaluator(res, gnd)
        er = pe.pairing()
        praf = pe.hitd_praf(er)
        self.elog.info("Doer: evaluation")
        return praf

    def rundown(self):
        fids = self.__reduced_frames()
        gnd = self.__gnd_mpairs()
        mre = self.__matching(fids, .9)
        praf = self.__evaluation(mre, gnd)
        print praf
