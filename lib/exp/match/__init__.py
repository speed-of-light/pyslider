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
        self.fx = Featx(self.root, self.name)
        self.set_match_core()
        self.set_featx()

    def __klass_var(self):
        st = "{}_{}".format(self.fx.klass_var, self.mcore)
        self.klass_var = st
        self.elog.info("Current configs: {}".format(st))

    def set_featx(self, engine="keypoint", method="SIFT"):
        """
        Refer to Featx.set_algorithm for more info
        """
        self.fx.set_algorithm(engine, method)
        self.__klass_var()

    def set_match_core(self, fn="FlannBased"):
        """
        BruteForce BruteForce-L1
        BruteForce-Hamming BruteForce-Hamming(2)
        FlannBased
        """
        self.mcore = fn
        self.elog.info("Use matching core: {}".format(fn))
        self.__klass_var()

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
        fxp = self.fx.get_feats_pair(sid, fid)
        mat = cv2.DescriptorMatcher_create(self.mcore)
        mra = mat.knnMatch(fxp["sd"], fxp["fd"], k=2)
        mra = self.__remove_high_simi(mra, thres)
        mdf = self.__to_df(mra)
        return dict(sid=sid, fid=fid, match=mdf)

    def __matching(self, feats, matcher, thres):
        mra = matcher.knnMatch(feats["sd"], feats["fd"], k=2)
        mra = self.__remove_high_simi(mra, thres)
        mdf = self.__to_df(mra)
        return mdf

    def __match_log(self, sid, fid, df):
        self.elog.info("{} - {}: {}".format(sid, fid, len(df)))

    def group_match(self, sids, fids, thres=0.8):
        self.__klass_var()
        ma = cv2.DescriptorMatcher_create(self.mcore)
        for sid in sids:
            for fid in fids:
                fxp = self.fx.get_feats_pair(sid, fid)
                df = self.__matching(fxp, ma)
                self.__match_log(sid, fid, df)
