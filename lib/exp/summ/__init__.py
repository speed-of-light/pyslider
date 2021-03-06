import pandas as pd
from lib.exp.featx import Featx
from lib.exp.pairing import PairFeats
from lib.exp.xframes import xFrames
from lib.exp.evaluator.xframes import XframeEval
from storage import _Storage as Stg


class Mary(object):
    root = "univ_07"
    names = ["coates", "chaves", "rozenblit"]

    def __init__(self):
        """
        A final sum-mary class
        """
        pass

    def __load_cp(self, name, key="result"):
        fx = Featx(self.root, name)
        pf = PairFeats(fx)
        xf = xFrames(pf)
        xfe = XframeEval(xf)
        df = xfe.load(key)
        df["dsn"] = name
        return df

    def __load_saf(self, name):
        fx = Featx(self.root, name)
        pf = PairFeats(fx)
        xf = xFrames(pf)
        df = xf.load("slide_ans_9")
        df["dsn"] = name
        print len(df)
        return df

    def df_classify_perf(self, key="result"):
        """
        Return classified performance data set
        """
        lcf = lambda n: self.__load_cp(n, key=key)
        return reduce(lambda x, y: x.append(y), map(lcf, self.names))

    def df_rec_ans(self):
        return reduce(lambda x, y: x.append(y), map(self.__load_saf, self.names))

    def get_storage(self):
        da = []
        for ns in self.names:
            stg = Stg(self.root, ns)
            da.append(stg.sd)
        return pd.DataFrame(da)

    def save(self, key, df):
        df.to_hdf(
            "./data/sumy.h5", key, mode='a', data_columns=True,
            format='t', complib='blosc', complevel=6)

    def load(self, key):
        df = pd.read_hdf("./data/sumy.h5", key, format='t')
        return df
