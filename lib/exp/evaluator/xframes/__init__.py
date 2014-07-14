from lib.exp.base import ExpCommon
from lib.exp.tools.preloader import Preloader as Pldr
from ground_truth import GroundTruth as GT
from accuracy import Accuracy


class XframeEval(Pldr, ExpCommon):
    def __init__(self, xf):
        ExpCommon.__init__(self, xf.root, xf.name)
        Pldr._preload(self, "gnd")
        self.xf_ = xf
        self.preview = True

    def _reload(self, module="gnd"):
        if module == "gnd":
            mod = GT(self.root, self.name)

    def cross_result(self, data, dkey="mean"):
        gkey = "{}_gnd".format(dkey)
        data[gkey] = map(self.gnd.answer, data["fid"].values)

    def cross_results(self, data, dkeys=["mean"]):
        crd = lambda k: self.cross_result(data, k)
        map(crd, dkeys)

    def __counting(self, df, akey, gkey):
        predict_no_slide = (df[akey] == 1)
        ground_no_slide = (df[gkey] == -1)
        predict_slide = (df[akey] == 0)
        ground_slide = (df[gkey] > 0)
        tn = len(df[predict_no_slide & ground_no_slide])
        fn = len(df[predict_no_slide & ground_slide])
        tp = len(df[predict_slide & ground_slide])
        fp = len(df[predict_slide & ground_no_slide])
        return dict(tn=tn, fn=fn, tp=tp, fp=fp)

    def __count_by_keys(self, df, name="no_name", key="mean"):
        ak = "{}_ans".format(key)
        gk = "{}_gnd".format(key)
        binn = self.__counting(df, ak, gk)
        binn.update(name=name, key=key)
        if self.preview:
            print binn
        return binn

    def __core(self, kn, df):
        keys = ["mean", "qart", "top"]
        self.cross_results(df, dkeys=keys)
        ckf = lambda k: self.__count_by_keys(df, name=kn, key=k)
        return map(ckf, keys)

    def roc_details(self, keys=[1, 2, 3]):
        bs = [self.__core(k, d) for k, d in self.xf_.crossing(keys)]
        bs = reduce(lambda x, y: x+y, bs)
        acc = Accuracy(bs, self.preview)
        return acc.details(acc.Common_Details+["fdr", "speficity"])

    def timer(self, keys=[1, 2, 3]):
        bs = [self.__core(k, d) for k, d in self.xf_.crossing(keys)]
        bs = reduce(lambda x, y: x+y, bs)
        acc = Accuracy(bs, self.preview)
        return acc.details(acc.Common_Details+["fdr", "speficity"])
