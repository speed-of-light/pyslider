import numpy as np
from exp.prepare import Prepare
from exp.feats import Feats
from exp.matching import Matcher
from exp.evaluator.ground_truth import GroundTruth


class Doer(object):
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.feats = Feats(root, name)
        self.matcher = Matcher(root, name)

    def __reduced_frames(self):
        pp = Prepare(self.root, self.name)
        df = pp.load('keys')
        pk = df[df.key.str.contains('reduce')].key.values[5]
        fids = pp.load(pk).frame_id.values.astype(np.int32)
        return fids

    def __gnd_mpairs(self):
        """
        load ground truth matched pairs
        """
        gt = GroundTruth(self.root, self.name)
        df = gt.univ_df()
        return df

    def rundown(self):
        pass
