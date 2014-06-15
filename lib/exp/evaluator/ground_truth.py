import pandas as pd
from ..base import ExpCommon
from ..summary import Summary
from base import DfExt


class GroundTruth(ExpCommon, Summary):
    def __init__(self, root, name):
        """
        Mainly designed to containing 3 dataframes:
            `abs_pairs`, `rel_pairs`, `segments`
        """
        ExpCommon.__init__(self, root, name)
        Summary.__init__(self)

    def univ_df(self):
        """
        Convert univ_df raw ground_truth to dataframe
        """
        coll = []
        gnd = "data/{}/{}/ground_truth".format(self.root, self.name)
        with open(gnd, 'r') as f:
            for ln in f.readlines():
                cols = [int(x) for x in ln.split(',')]
                coll.append(cols)
        gf = pd.DataFrame(data=coll,
                          columns=['fid', 'sid', 'slide_type', 'cam_status'])
        gcf = self.__aggregate(gf.copy())
        return gcf

    def __aggregate(self, df):
        """
        Get the univ aggregated result
        """
        f_slid = -1
        f_keep = -1
        f_cnt = 1
        for inx in df.index:
            if f_slid < 0:
                f_slid = df.ix[inx]['sid']
                continue
            if f_slid == df.ix[inx]['sid']:
                if f_cnt == 1:
                    f_cnt = 2
                    f_keep = inx
                    continue
                if f_cnt > 1:
                    df = df.drop(f_keep)
                f_keep = inx
            else:
                f_cnt = 1
                f_slid = df.ix[inx]['sid']
                continue
        return df

    def __ftyping(self, fsid, feid, ftype):
        if ftype == "duration":
            return feid - fsid
        elif ftype == "end":
            return feid

    def __ftuple(self, stat, ftp, gnd, ftype):
        if (stat == "init") or (stat == "singular"):
            ftv = self.__ftyping(gnd.fid, gnd.fid, ftype)
            return [gnd.fid, ftv, gnd.sid]
        elif stat == "found_pair":
            ftv = self.__ftyping(ftp[0], gnd.fid, ftype)
            ftp[1] = ftv
            return ftp

    def segments_df(self, df, ftype="duration"):
        """
        Return dataframe version of segments
        """
        segs = self.segments(df, ftype)
        cols = ['fstart', ftype, 'sid']
        df = pd.DataFrame(segs, columns=cols)
        return df

    def segments(self, df, ftype="duration"):
        """
        df: columns should be like `abs_pairs`.
        ftype: control the return data with "duration"(default) or
            just "end" frame id
        Return ground truth of segments, should return a list of
            [fstart, duration, sid]
        """
        f_start = -1
        seg = []  # segment for global use
        flp = [df.iloc[0].fid]  # segment for local use
        for si in df.index:
            gnd = df.ix[si]
            if f_start < 0:
                flp = self.__ftuple("init", flp, gnd, ftype)
                f_start = gnd.sid
            elif f_start == gnd.sid:
                flp = self.__ftuple("found_pair", flp, gnd, ftype)
                seg.append(flp[:])
                f_start = -1
            else:  # single point
                seg.append(flp[:])
                flp = self.__ftuple("singular", flp, gnd, ftype)
                f_start = gnd.sid
        if flp is not None:
            seg.append(flp[:])
        return seg

    def shrink(self, df):
        """
        df: `fid`, `sid` pairs
        Get shrink data from original matched pairs
        Return a cloned copy of original input
        example:
            df.sid = [1, 1,  1,  1,  2,  2,  3,  3,  4,  4]
            return should be [1, 2, 3, 4]
        """
        f_sid = -1
        ret = df.copy(deep=True)
        for di, dd in df.iterrows():
            if f_sid < 0:  # init
                f_sid = dd.sid
            elif f_sid == dd.sid:
                ret = ret.drop(di)
                continue
            elif f_sid != dd.sid:
                f_sid = dd.sid
        return ret

    def add_mark(self, df, sid=None, fid=None, ftype=None):
        """
        Add mark to dataframe table, **not saved**.
        df: should come from `abs_pairs`
        """
        db = DfExt(df)
        result = db.insert(sid, fid, ftype)
        return result
