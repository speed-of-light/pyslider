import pandas as pd
from lib.exp.summary import Summary
from lib.exp.evaluator.slide_coverage import SlideCoverage as Scov


class _Scov(Scov):
    def __init__(self, gnd, pre_ns=None, pre_ws=None):
        """
        pre_ns: preprocessing number of slides
        pre_ws: preprocessing number of switeches
        """
        Scov.__init__(self, gnd.load("segments"))
        self.__get_sn(gnd)
        self.prens = pre_ns if pre_ns else self.ns
        self.prews = pre_ws if pre_ws else len(self.gseg)

    def __get_sn(self, gnd):
        su = Summary()
        sin = su.info(gnd.root, gnd.name)
        self.ns = sin.n_slides

    def __cov_base(self, pdf, key):
        if len(pdf) == 0:
            return 0
        fdf = pdf[pdf[key].notnull() & (pdf[key] > 0)]
        ks = [gi for gi, gd in fdf.groupby(key)]
        return len(ks)*1.

    def __switch_cov(self, pdf):
        fs = self.__cov_base(pdf, "hit_seg_id")
        return dict(swc=fs/len(self.gseg), fix_swc=fs/self.prews)

    def __slide_cov(self, pdf):
        fs = self.__cov_base(pdf, "sid")
        return dict(slc=fs/self.ns, fix_slc=fs/self.prens)

    def __covs(self, df, appkey):
        akn = appkey[:-4]
        fdf = df[df[appkey] == 0]
        pdf = pd.DataFrame(map(self._mk_xdict, fdf.fid, fdf[akn]))
        dk = dict(key=akn)
        dk.update(self.__slide_cov(pdf))
        dk.update(self.__switch_cov(pdf))
        return dk

    def __each_cov(self, key, df):
        aks = filter(lambda x: "ans" in x, df.columns)
        sext = lambda x: self.__covs(df, x)
        ss = map(sext, aks)
        df = pd.DataFrame(ss)
        df["config"] = key
        return df

    def compute(self, plist):
        bs = [self.__each_cov(*pack) for pack in plist]
        rdf = reduce(lambda x, y: x.append(y), bs)
        rdf = rdf.reset_index(drop=1)
        return rdf
