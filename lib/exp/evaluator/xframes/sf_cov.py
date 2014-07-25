import pandas as pd
from lib.exp.evaluator.slide_coverage import SlideCoverage as Scov
from lib.exp.evaluator.accuracy import Accuracy


class _SFcov(Scov):
    COV = dict(sw="hit_seg_id", sl="sid")
    def __init__(self, gnd, presl=0, presw=0):
        self.gseg = gnd.load("segments")
        self.presl = presl
        self.presw = presw

    def __timeline_cov(self, df, ansk):
        pass

    def __cov_tp(self, r):
        return (r.ans == r.sid) & (r.ans > 0)

    def __cov_tn(self, r):
        return (r.ans == r.sid) & (r.ans < 0)

    def __cov_fp(self, r):
        return ((r.sid > 0) & (r.ans < 0)) | ((r.sid != r.ans) & (r.ans > 0))

    def __cov_fn(self, r):
        return (r.sid < 0) & (r.ans > 0)

    def __pop_set(self, key, df):
        tp = len(df[df.apply(self.__cov_tp, axis=1)])
        tn = len(df[df.apply(self.__cov_tn, axis=1)])
        fp = len(df[df.apply(self.__cov_fp, axis=1)])
        fn = len(df[df.apply(self.__cov_fn, axis=1)])
        return dict(key=key, name="", tp=tp, tn=tn, fp=fp, fn=fn)

    def __cov(self, sn="sw", key=None, df=None):
        tpf = df[df.apply(self.__cov_tp, axis=1)]
        uhi = [hi for hi, hd in tpf.groupby(self.COV[sn])]
        fhl = len(uhi)*1.
        pk = "pre{}".format(sn)
        kys = ["key", "{}cn".format(sn), "{}c".format(sn), "f{}c".format(sn)]
        print pk, self.__dict__[pk], fhl, len(df)
        vls = [key, len(uhi), fhl/len(self.gseg), fhl/self.__dict__[pk]]
        return dict(zip(kys, vls))

    def __accuracy(self, keys, covl):
        ps = map(self.__pop_set, keys, covl)
        acc = Accuracy(ps, preview=False)
        return acc.details(acc.Common_Details+["speficity"])

    def __swcov(self, keys, covl):
        swcov = lambda k, df: self.__cov("sw", k, df)
        return pd.DataFrame(map(swcov, keys, covl))

    def __slcov(self, keys, covl):
        slcov = lambda k, df: self.__cov("sl", k, df)
        return pd.DataFrame(map(slcov, keys, covl))

    def batch_detail(self, akl, ansl):
        adf = self.__accuracy(akl, ansl)
        swf = self.__swcov(akl, ansl)
        slf = self.__slcov(akl, ansl)
        df = adf.merge(swf, on="key")
        df = df.merge(slf, on="key")
        return df

    def __raw_covs(self, df, ak):
        fdf = df[df[ak] > 0]
        pdf = pd.DataFrame(map(self._mk_xdict, fdf.fid, fdf[ak]))
        return pdf

    def compute(self, adf):
        ks = filter(lambda y: "ans" in y, adf.columns)
        rcf = lambda ak: self.__raw_covs(adf, ak)
        ansl = map(rcf, ks)
        af = self.batch_detail(ks, ansl)
        return af
