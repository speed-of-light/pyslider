from lib.exp.featx import Featx
from lib.exp.pairing import PairFeats
from lib.exp.xframes import xFrames
from lib.exp.evaluator.xframes import XframeEval


class Mary(object):
    root = "univ_07"
    names = ["coates", "chaves", "rozenblit"]

    def __init__(self):
        """
        A final sum-mary class
        """
        pass

    def __load_cp(self, name):
        fx = Featx(self.root, name)
        pf = PairFeats(fx)
        xf = xFrames(pf)
        xfe = XframeEval(xf)
        df = xfe.load("result")
        df["dsn"] = name
        return df

    def df_classify_perf(self):
        """
        Return classified performance data set
        """
        return map(self.__load_cp, self.names)
