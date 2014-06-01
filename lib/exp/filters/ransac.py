import numpy as np
import cv2


class Ransac(object):
    def __init__(self):
        pass

    def _matched_points(self, kps, mps):
      rr = [kps[m].pt for m in mps]
      return np.float32(rr).reshape(-1, 1, 2)

    def compute(self, good, skp, vkp, min_matches=10):
        """
        data is a dict contained columns:
        [ 'kp_train', 'kp_test', 'matches']
        Methods:
          0 - a regular method using all the points
          CV_RANSAC - RANSAC-based robust method
          CV_LMEDS - Least-Median robust method
        """
        if len(good) >= min_matches:
            src = self._matched_points(skp, good.qix)
            des = self._matched_points(vkp, good.tix)
            M, mask = cv2. \
                findHomography(src, des,
                               method=cv2.RANSAC,
                               ransacReprojThreshold=5.0)
            return M, mask
        return None

    def get_bound_img(self, fimg, simg, homo):
        """
        Return homographic array of image result
        Params:
            fimg: img array of frames
            simg: img array of slide
            homo: transformation matrix (usually 9*9)
        """
        h, w, z = simg.shape
        pos = [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
        bnd = np.float32(pos).reshape(-1, 1, 2)
        bound = cv2.perspectiveTransform(bnd, homo)
        rimg = fimg[:]
        cv2.polylines(rimg, [np.int32(bound)], True, (0, 255, 0), 3)
        return rimg
