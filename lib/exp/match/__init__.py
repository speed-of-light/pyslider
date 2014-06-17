__doc__ = """
Perform feature matching on features
"""

__all__ = []

import cv2
import pandas as pd
from lib.exp.base import ExpCommon
from lib.exp.featx import Featx


class Matchx(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        self.set_match_core("FlannBased")

    def set_match_core(self, fn):
        """
        BruteForce BruteForce-L1
        BruteForce-Hamming BruteForce-Hamming(2)
        FlannBased
        """
        self.mcore = fn
        self.elog.info("Use matching core: {}".format(fn))

    def __remove_high_simi(self, matches, thres=.5):
        """
        Remove high similarity pairs
        """
        mre = []
        for m, n in matches:
            if m.distance < n.distance*thres:
                mre.append(m)
        return mre

    def __flatten_matches(self, matches):
        mra = []
        for m in matches:
            mra.append([m.queryIdx, m.trainIdx, m.imgIdx, m.distance])
        return mra

    def __to_df(self, data):
        col = ["qix", "tix", "iix", "dt"]
        if len(data) is 0:
            df = pd.DataFrame(columns=col)
        else:
            fm = self.__flatten_matches(data)
            df = pd.DataFrame(fm, columns=col)
        return df

    def match(self, sid, fid, thres=0.8):
        fx = Featx(self.root, self.name)
        fxp = fx.get_feats_pair(sid, fid)
        mat = cv2.DescriptorMatcher_create(self.mcore)
        mra = mat.knnMatch(fxp["sd"], fxp["fd"], k=2)
        mra = self.__remove_high_simi(mra, thres)
        mdf = self.__to_df(mra)
        return dict(sid=sid, fid=fid, match=mdf)
