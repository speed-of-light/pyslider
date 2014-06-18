import pandas as pd
from lib.exp.summary import Summary
from lib.exp.pre import Reducer


class Mahelp(object):
    def __init__(self):
        pass

    def __dvz(self, sa, sb):
        if sa == 0:
            return 0
        else:
            return sa*1.0/sb

    def __get_stats(self, skl, fkl, df, time):
        dm = df["dist"].mean()
        skr = self.__dvz(len(df), skl)
        fkr = self.__dvz(len(df), fkl)
        return [dm, skr, fkr, time]

    def __flatten_matches(self, matches):
        mra = []
        for m in matches:
            mra.append([m.queryIdx, m.trainIdx, m.imgIdx, m.distance])
        return mra

    def _match_info(self, sid, fid, fxp, mat, time):
        skl = len(fxp["sk"])
        fkl = len(fxp["fk"])
        pairs = [sid, fid]
        lens = [skl, fkl, len(mat)]
        info = self.__get_stats(skl, fkl, mat, time)
        return dict(pairs=pairs, lens=lens, info=info)

    def _info_str(self, pairs=None, lens=None, info=None, time=None):
        ps = "[{: 2d}-{:5d}]".format(*pairs)
        cs = ": {:4d}sk {:4d}fk {:4d}matches.".format(*lens)
        ifs = "{:7.3f}dist_avg, ssc:{:5.2f} fsc:{:5.2f}, ms:{: 8.3f}".format(*info)
        return "{}{} | {}".format(ps, cs, ifs)

    def _remove_high_simi(self, matches, thres=.5):
        """
        Remove high similarity pairs
        """
        mre = []
        for m, n in matches:
            if m.distance < n.distance*thres:
                mre.append(m)
        return mre

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
