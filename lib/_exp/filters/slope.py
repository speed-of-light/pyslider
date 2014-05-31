from core import KpFilter


class Slope(KpFilter):
    """
    Use matching pair slopes distribution to filter out bad results
    """
    def __init__(self):
        pass

    def _slope(self, spt, fpt):
        """
        Get slope from 2 points
        """
        dx = fpt[0] - spt[0]
        dy = fpt[1] - spt[1]
        return dy*1.0/dx

    def _slopes(self, skps, fkps, good):
        """
        Getting matches slope list
        skp: slide keypoints
        fkp: frame keypoints
        """
        fpt = fkps[int(good.tix)].pt
        spt = skps[int(good.qix)].pt
        ss = self._slope(spt, fpt)
        return ss

    def get_slopes(self, ret):
        """
        ret is dict contains: [matches, sif, vif]
        """
        good = ret['matches']
        good['slope'] = good.apply(lambda matches: self._slopes(
            ret['sif']['kps'], ret['vif']['kps'], matches), axis=1)
        return good

    def result(self, good, sigma=.5):
        """
        sigma: tolerance of input slopes
        """
        smean = good.slope.mean()
        sstd = good.slope.std()*sigma
        bot = smean - sstd
        top = smean + sstd
        return good[(good['slope'] >= bot) & (good['slope'] <= top)]

    def gridise(self):
        """
        Use gridize image to determine matched pairs
        """
        pass
