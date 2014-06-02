import cv2
from core import KpFilter


class Slope(KpFilter):
    """
    Use matching pair slopes distribution to filter out bad results
    """
    def __init__(self, data):
        KpFilter.__init__(self, data)

    def __slope(self, spt, fpt):
        """
        Get slope from 2 points
        """
        dx = fpt[0] - spt[0]
        dy = fpt[1] - spt[1]
        return dy*1.0/dx

    def __slopes(self, skps, fkps, good):
        """
        Getting matches slope list
        skp: slide keypoints
        fkp: frame keypoints
        """
        fpt = fkps[int(good.tix)].pt
        spt = skps[int(good.qix)].pt
        ss = self.__slope(spt, fpt)
        return ss

    def __keeper(self, match, bot, top):
        val = -1
        if match.slope >= bot and match.slope <= top:
            val = 1
        else:
            val = 0
        return val

    def __get_slopes(self, ret):
        """
        ret is dict contains: [matches, sif, vif]
        """
        good = ret['matches']
        good['slope'] = good.apply(lambda matches: self.__slopes(
            ret['sif']['kps'], ret['vif']['kps'], matches), axis=1)
        return good

    def __roi(self, tl, br):
        """
        Return quadrant order rectangle
        """
        y = 1
        x = 0
        tr = (tl[y], br[x])
        bl = (tl[x], br[y])
        return (tr, tl, bl, br)

    def __unknown_roi(self, roi):
        return (roi is None) or (roi == -1)

    def __mark_roi(self, row, ii, roi):
        """
        keep if point is inside or on the edge of roi
        """
        kps = self.data['sif']['kps']
        pt = kps[row.qix].pt
        ppr = cv2.pointPolygonTest(roi, pt, measureDist=False)
        roid = -1
        if ppr >= 0 and self.__unknown_roi(row.roi):
            roid = ii
        return roid

    def __get_slope_range(self, slopes, sigma):
        mean = slopes.mean()
        sstd = slopes.std()*sigma
        bot = mean - sstd
        top = mean + sstd
        return bot, top

    def get_rois(self, hash_cross):
        """
        qsize: size of input image (slide)
        hash_cross: four cross points of a hash (Quadrant order)
        return roi:
           _0_|_3_|_6_
           _1_|_4_|_7_
            2 | 5 | 8
        """
        x = 0
        y = 1
        qsize = self.data['qsize']
        xmax = qsize[x]
        ymax = qsize[y]
        hc = hash_cross
        roi = []
        roi.append(self.__roi((0, 0), hc[1]))
        roi.append(self.__roi((0, hc[1][y]), hc[2]))
        roi.append(self.__roi((0, hc[2][y]), (hc[2][x], ymax)))
        roi.append(self.__roi((hc[1][x], 0), hc[0]))
        roi.append(self.__roi(hc[1], hc[3]))
        roi.append(self.__roi(hc[2], (hc[3][x], ymax)))
        roi.append(self.__roi((hc[0][x], 0), (xmax, hc[0][y])))
        roi.append(self.__roi(hc[0], (xmax, hc[3][y])))
        roi.append(self.__roi(hc[3], qsize))
        return roi

    def filter_(self, rois, sigma=.5):
        """
        sigma: tolerance of input slopes
        roi: a set of regions to be check
        Return original dataframe with a `keep` column to indicate keep data
        or not.
        """
        good = self.data['matches']
        bot, top = self.__get_slope_range(good.slope, sigma)
        if rois is None:
            fl = lambda row: self.__keeper(row, bot, top)
            good['keep'] = good.apply(fl, axis=1)
        elif isinstance(rois, list):
            for roi in rois:
                fl = lambda row: self.__is_in_roi(row, roi)
                good['keep'] = good.apply(fl, axis=1)
        return good

    # TODO: add gridize filter result
    def gridise(self):
        """
        Use gridize image to determine matched pairs
        """
        pass
