import pandas as pd
from lib.exp.summary import Summary
from lib.exp.pre import Reducer


class Mahelp(object):
    def __init__(self):
        pass

    def _info_str(self, pairs, lens, info):
        ps = "[{}-{}]".format(*pairs)
        cs = "{: 4d} sk {: 4d} fk {: 4d} matches.".format(*lens)
        ifs = "{:7.3f} avg-dist, ssc: {:5.2f} fsc: {:5.2f}".format(*info)
        return "{}: {} | {}".format(ps, cs, ifs)

    def _remove_high_simi(self, matches, thres=.5):
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

    def _to_df(self, data):
        col = ["qix", "tix", "iix", "dist"]
        if len(data) is 0:
            df = pd.DataFrame(columns=col)
        else:
            fm = self.__flatten_matches(data)
            df = pd.DataFrame(fm, columns=col)
        return df

    def seeds(self, key="/reduce/diff_next/size_30"):
        su = Summary()
        sids = range(1, su.info(self.root, self.name).n_slides+1)
        rr = Reducer(self.root, self.name)
        fids = rr.frame_ids(key)
        return sids, fids
