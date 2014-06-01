import numpy as np
import cv2


class Ransac(object):
    def __init__(self, data):
        self.data = data

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

    def compute(self, min_matches=10):
        good = self.data['matches']
        skp = self.data['sif']['kps']
        fkp = self.data['vif']['kps']
        M, mask = self.__compute(good, skp, fkp, min_matches=min_matches)
        self.data['matches']['keep'] = mask
        return M
