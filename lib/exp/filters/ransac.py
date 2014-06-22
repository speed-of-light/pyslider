import numpy as np
import cv2
from core import FilterBase


class Ransac(FilterBase):
    def __init__(self, matchx):
        FilterBase.__init__(self, matchx)

    def __good_pts(self, kps, mps):
        rr = [kps[m].pt for m in mps]
        return np.float32(rr).reshape(-1, 1, 2)

    def __compute(self, good=None, skps=None, fkps=None, min_matches=10):
        """
        data is a dict contained columns:
        [ 'kp_train', 'kp_test', 'matches']
        Methods:
          0 - a regular method using all the points
          CV_RANSAC - RANSAC-based robust method
          CV_LMEDS - Least-Median robust method
        """
        if len(good) >= min_matches:
            src = self.__good_pts(skps, good.qix)
            des = self.__good_pts(fkps, good.tix)
            M, mask = cv2.\
                findHomography(src, des,
                               method=cv2.RANSAC,
                               ransacReprojThreshold=5.0)
            return M, mask
        return None, []

    def filter_pair(self, sid=None, fid=None, df=None, min_matches=10):
        data = FilterBase.pair_data(self, sid, fid, df)
        M, mask = self.__compute(min_matches=min_matches, **data)
        return M, mask

    def filter_pairs(self, start=0, size=-1, min_matches=10):
        """
        Returned by-product: M, the homography boundary
        """
        self.data = []
        end = start + size
        for mat in self.matchx.matches[start: end]:
            homo, mask = self.filter_pair(min_matches=min_matches, **mat)
            dm = dict(homo=homo, keep=mask, matches=mat["df"], sid=mat["sid"],
                      fid=mat["fid"])
            self.data.append(dm)

    def new_matches(self):
        ret = []
        for rd in self.data:
            mat = []
            kep = rd["keep"]
            if len(kep) > 0:
                mat = rd["matches"][kep == 1]
            keg = dict(sid=rd["sid"], fid=rd["fid"], df=mat)
            ret.append(keg)
        return ret
