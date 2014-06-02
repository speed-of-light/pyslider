import cv2
import numpy as np
from core import KpFilter


class Slope(KpFilter):
    """
    Use matching pair slopes distribution to filter out bad results
    """
    def __init__(self, data):
        KpFilter.__init__(self, data)
        self.__update_matches()

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

    def __update_matches(self):
        good = self.data['matches']
        self.__get_slopes(good)
        self.data['matches'] = good

    def __get_slopes(self, good, update=True):
        """
        ret is dict contains: [matches, sif, vif]
        """
        if update:
            skp = self.data['sif']['kps']
            fkp = self.data['vif']['kps']
            lm = lambda matches: self.__slopes(skp, fkp, matches)
            good['slope'] = good.apply(lm, axis=1)
        return good

    def __roi(self, tl, br):
        """
        Return quadrant order rectangle
        """
        y = 1
        x = 0
        tr = (br[x], tl[y])
        bl = (tl[x], br[y])
        return (tr, tl, bl, br)

    def __unknown_roi(self, row):
        return ('roi' not in row.keys()) or (row.roi is None) or (row.roi == -1)

    def __mark_roi(self, row, ii, roi):
        """
        keep if point is inside or on the edge of roi
        """
        kps = self.data['sif']['kps']
        pt = kps[int(row.qix)].pt
        nroi = np.array(roi)
        ppr = cv2.pointPolygonTest(nroi, pt, measureDist=False)
        if self.__unknown_roi(row):
            roid = -1
            if ppr >= 0:
                roid = ii
        else:
            roid = row.roi
        return roid

    def __get_slope_range(self, slopes, sigma):
        mean = slopes.mean()
        sstd = slopes.std()*sigma
        bot = mean - sstd
        top = mean + sstd
        return bot, top

    def __good_keeper(self, good, sigma):
        bot, top = self.__get_slope_range(good.slope, sigma)
        fl = lambda row: self.__keeper(row, bot, top)
        good['keep'] = good.apply(fl, axis=1)
        return good

    def __check_slope(self):
        good = self.data['matches']
        if 'slope' not in good.columns:
            good = self.__get_slopes(good, True)
        return good

    def __get_rois(self, hash_cross):
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
        xmax = qsize[y]
        ymax = qsize[x]
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
        roi.append(self.__roi(hc[3], (xmax, ymax)))
        return roi

    def filter_(self, rois=None, sigma=.5):
        """
        sigma: tolerance of input slopes
        roi: a set of regions to be check
        Return original dataframe with a `keep` column to indicate keep data
        or not.
        """
        good = self.__check_slope()
        if rois is None:
            self.__good_keeper(good, sigma)
        elif isinstance(rois, list):
            if 'roi' in good.columns:
                del good['roi']
            for ii, roi in enumerate(rois):
                fl = lambda row: self.__mark_roi(row, ii, roi)
                good["roi"] = good.apply(fl, axis=1)
            for rv, fg in good.groupby('roi'):
                self.__good_keeper(fg, sigma)
                good.loc[good.index.isin(fg.index), "keep"] = fg.keep
                print rv, len(fg)
        return good

    def __martin(self, margin):
        """
        Transform original margin to computed easier values
        """
        margin[1] = 1 - margin[1]
        margin[2] = 1 - margin[2]
        return margin

    def __hash_margin(self, margin):
        """
        margin: top right bottom left, but in !!ratio!!
        """
        mt = self.__martin(margin)
        qsize = self.data['qsize']
        qx = qsize[1]
        qy = qsize[0]
        hcs = []
        hcs.append((int(qx*mt[1]), int(qy*mt[0])))
        hcs.append((int(qx*mt[3]), int(qy*mt[0])))
        hcs.append((int(qx*mt[3]), int(qy*mt[2])))
        hcs.append((int(qx*mt[1]), int(qy*mt[2])))
        return hcs

    def gridise(self, htype='tri'):
        """
        Use gridize image to determine matched pairs
        htype: the split ratio of cross points for a hash.
            use a four elements array to custom cross region
        Return `hashes` for plot use, `rois` for filtering use
        """
        if htype == 'tri':
            hashes = self.__hash_margin([1.0/3]*4)
        elif htype == 'main':
            hashes = self.__hash_margin([.15, .15, .15, .15])
        else:  # custom
            hashes = self.__hash_margin(htype)
        rois = self.__get_rois(hashes)
        return hashes, rois
