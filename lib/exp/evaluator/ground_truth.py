import pandas as pd
from lib.exp.base import ExpCommon


class GroundTruth(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)

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

    def segments(self, df, ftype="duration"):
        """
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

    def pairs(self):
        """
        TODO add this
        """
        self.save
        pass
