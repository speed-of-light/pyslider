import numpy as np
from base import ExpCommon
from prepare import Prepare
from matching import Matcher
from evaluator.ground_truth import GroundTruth


class Doer(ExpCommon):
    def __init__(self, root, name):
        self.root = root
        self.name = name

    def __reduced_frames(self):
        """ Get preprocessed frames """
        pp = Prepare(self.root, self.name)
        df = pp.load('keys')
        pk = df[df.key.str.contains('reduce')].key.values[5]
        fids = pp.load(pk).frame_id.values.astype(np.int32)
        return fids

    def __gnd_mpairs(self):
        """
        load ground truth matched pairs
        TODO change univ_df() to pairs()
        """
        gt = GroundTruth(self.root, self.name)
        df = gt.univ_df()
        return df

    def __matching(self, fids, thres):
        mm = Matcher(self.root, self.name)
        res, sfs, vfs = mm.set_match(fids, ransac=False, thres=0.9)

    def rundown(self):
        pass