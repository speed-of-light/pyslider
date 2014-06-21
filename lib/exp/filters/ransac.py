import numpy as np
import cv2
from base import FilterBase


class Ransac(FilterBase):
    def __init__(self, data):
        FilterBase.__init__(self, data)

    def __good_pts(self, kps, mps):
        rr = [kps[m].pt for m in mps]
        return np.float32(rr).reshape(-1, 1, 2)

    def __compute(self, good, skp, vkp, min_matches=10):
        """
        data is a dict contained columns:
        [ 'kp_train', 'kp_test', 'matches']
        Methods:
          0 - a regular method using all the points
          CV_RANSAC - RANSAC-based robust method
          CV_LMEDS - Least-Median robust method
        """
        if len(good) >= min_matches:
            src = self.__good_pts(skp, good.qix)
            des = self.__good_pts(vkp, good.tix)
            M, mask = cv2.\
                findHomography(src, des,
                               method=cv2.RANSAC,
                               ransacReprojThreshold=5.0)
            return M, mask
        return None, None

    def filtering(self, min_matches=10):
        """
        Returned by-product: M, the homography boundary
        """
        good, skp, fkp = FilterBase.filtering(self)
        M, mask = self.__compute(good, skp, fkp, min_matches=min_matches)
        self.data['matches']['keep'] = mask
        return M
