from lib.exp.evaluator.accuracy import Accuracy
import inflection as Inf


class RocDetail(object):
    def __init__(self):
        pass

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
        gk = "{}_gnd".format(key[:-4])
        binn = self.__counting(df, key, gk)
        binn.update(name=name, key=Inf.titleize(key))
        if self.preview:
            print binn
        return binn

    def __core(self, kn, df):
        keys = filter(lambda c: "ans" in c, df.columns)
        self.cross_results(df, dkeys=keys)
        ckf = lambda k: self.__count_by_keys(df, name=kn, key=k)
        return map(ckf, keys)

    def roc_details(self, keys=[1, 2, 3]):
        bs = [self.__core(k, d) for k, d in self.xf_.rev_crossing(keys)]
        bs = reduce(lambda x, y: x+y, bs)
        acc = Accuracy(bs, self.preview)
        return acc.details(acc.Common_Details+["fdr", "speficity"])
