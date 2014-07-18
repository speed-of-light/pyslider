import cv2
import pandas as pd
import numpy as np
from lib.exp.summary import Summary


class _Core(object):
    _mkeys = ["ski", "fki", "iix", "dist"]

    def __init__(self, root=None, name=None, bbft=0.8, thres=5.0,
                 mm=10, homo=False, area=False, invw=False, octaf=0):
        self.bbft = bbft
        self.thres = thres
        self.minmat = mm
        self.homo = homo
        self.area = area
        self.invw = invw
        self.__homo_method()
        self.__get_imsize(root, name)

    def __homo_method(self):
        if self.thres:
            hm = cv2.RANSAC
        elif self.homo:
            hm = 0
        else:
            hm = None
        self.hm = hm

    def __base_area(self):
        h, w = self.imsize
        pts = np.float32([ [0, 0], [0, h-1], [w-1, h-1], [w-1, 0] ]).\
            reshape(-1, 1, 2)
        self.base_area = cv2.contourArea(pts)

    def __get_imsize(self, root, name):
        su = Summary()
        sin = su.info(root, name)
        self.imsize = (sin.v_height, sin.v_width)
        self.__base_area()

    def __xpts(self, sx, fx):
        lk = lambda df: df[['x', 'y']]
        return lk(sx), lk(fx)

    def __good_pts(self, mkp, skp, fkp):
        remap = lambda ar: np.float32(ar).reshape(-1, 1, 2)
        return remap([skp.iloc[m] for m in mkp.ski]), \
               remap([fkp.iloc[m] for m in mkp.fki])

    def __get_area(self, m):
        if m is None:
            return 0
        h, w = self.imsize
        pts = np.float32([ [0, 0], [0, h-1], [w-1, h-1], [w-1, 0] ]). \
            reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, m)
        return cv2.contourArea(dst)

    def __compute(self, good, skp, fkp):
        """
        Methods:
          0 - a regular method using all the points
          CV_RANSAC - RANSAC-based robust method
          CV_LMEDS - Least-Median robust method
        """
        if len(good) >= self.minmat:
            src, des = self.__good_pts(good, skp, fkp)
            M, mask = cv2.findHomography(
                 src, des, method=self.hm,
                 ransacReprojThreshold=self.thres)
            return M, mask.ravel().tolist()
        return None, [0]*len(good)

    def __inv(self, data):
        if self.invw:
            data[data == 1] = -10**self.invw
            data[data == 0] = 1
        return data

    def __homo_core(self, gd, sx, fx):
        """
        Returned by-product: M, the homography boundary
        """
        spt, fpt = self.__xpts(sx["kps"], fx["kps"])
        M, gd_in_homo = self.__compute(gd, spt, fpt)
        if self.area:
            gd["area"] = self.__get_area(M)
            gd["barea"] = self.base_area
        gd["ransac"] = self.__inv(gd_in_homo)
        return gd

    def __homography(self, good, sx, fx):
        if self.hm is not None:
            gdr = self.__homo_core(good, sx, fx)
        else:
            gdr = good
        return gdr

    def __reject_dist_ratio(self, m, n):
        """
        According to wiki:
            thres: greater than 0.8, which eliminates 90% of the false matches
            while discarding less than 5% of the correct matches
        """
        if m.distance < n.distance*self.bbft:
            return m
        return None

    def __best_bin_first(self, matches):
        """
        Remove high similarity pairs
          Beis, J., and Lowe, D.G "Shape indexing using approximate nearest-
          neighbour search in high-dimensional spaces", Conference on Computer
          Vision and Pattern Recognition, Puerto Rico, 1997, pp. 1000-1006
        """
        not_non = lambda v: v is not None
        rejector = lambda (m, n): self.__reject_dist_ratio(m, n)
        return filter(not_non, map(rejector, matches))

    def __to_matches_df(self, data):
        """
        `ski`: slide keypoint index
        `fki`: frame keypoint index
        """
        if len(data) is 0:
            df = pd.DataFrame(columns=self._mkeys)
        else:
            dflator = lambda m: [m.queryIdx, m.trainIdx, m.imgIdx, m.distance]
            fm = map(dflator, data)
            df = pd.DataFrame(fm, columns=self._mkeys)
        return df

    def pairing(self, matches, slide, frame):
        mlist = self.__best_bin_first(matches)
        mdf = self.__to_matches_df(mlist)
        if len(mdf) > 0:
            mdf = self.__homography(mdf, slide, frame)
        return mdf
