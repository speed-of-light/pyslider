from core import KpFilter


class Slope(KpFilter):
    """
    Use matching pair slopes distribution to filter out bad results
    """
    def __init__(self):
        pass

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

    def filter(self, good, sigma=.5):
        """
        sigma: tolerance of input slopes
        Return original dataframe with a `keep` column to indicate keep data
        or not.
        """
        smean = good.slope.mean()
        sstd = good.slope.std()*sigma
        bot = smean - sstd
        top = smean + sstd
        good['keep'] = good.apply(lambda row:
                                  self.__keeper(row, bot, top), axis=1)
        return good

    # TODO: add gridize filter result
    def gridise(self):
        """
        Use gridize image to determine matched pairs
        """
        pass
