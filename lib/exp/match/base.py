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

    def frame_seeds(self, key="/reduce/diff_next/size_30"):
        rr = Reducer(self.root, self.name)
        fids = rr.frame_ids(key)
        return fids

    def _rtlog_cols(self):
        return ["sid", "fid", "skcnt", "fkcnt", "mrcnt",
                "mean_dist", "ssc", "fsc", "time"]

    def _mem_rtlog(self, pairs=None, lens=None, info=None):
        pairs.extend(lens)
        pairs.extend(info)
        ldf = pd.DataFrame([pairs], columns=self._rtlog_cols())
        if hasattr(self, "rtlog"):
            self.rtlog = self.rtlog.append(ldf)
        else:
            self.rtlog = ldf

    def _match_info(self, mat, time,
                    sid=None, fid=None, sk=None, fk=None):
        skl = len(sk)
        fkl = len(fk)
        pairs = [sid, fid]
        lens = [skl, fkl, len(mat)]
        info = self.__get_stats(skl, fkl, mat, time)
        return dict(pairs=pairs, lens=lens, info=info)

    def _info_str(self, pairs=None, lens=None, info=None, time=None):
        ps = "[{: 2d}-{:5d}]".format(*pairs)
        cs = ": {:4d}sk {:4d}fk {:4d}matches.".format(*lens)
        ifs = "{:5.2f} dist_avg, ssc:{:4.2f} \
                fsc:{:4.2f}, ms:{:5.2f}".format(*info)
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

    def _pair_key(self, sid, fid):
        return "m_{:03d}_{:03d}".format(sid, fid)

    def batch_save(self):
        self.save("rtlog", self.rtlog)
        for sm in self.matches:
            key = self._pair_key(sm["sid"], sm["fid"])
            self.save(key, sm["df"])

    def slide_seeds(self):
        su = Summary()
        sids = range(1, su.info(self.root, self.name).n_slides+1)
        return sids

    def seeds(self, key="/reduce/diff_next/size_30"):
        sids = self.slide_seeds()
        fids = self.frame_seeds(key)
        return sids, fids
