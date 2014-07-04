import pandas as pd
from accuracy_data_extractor import PreSegHrBins


class __AccExtractors(object):
    PreprocessSegmentHitRatio = PreSegHrBins


class Accuracy(__AccExtractors):
    def __init__(self):
        """
        Usage example:
            acc = Accuracy()
            acc.set_data(data, caller)
            acc.detail("accuracy")
        """
        pass

    def set_data(self, root, name, extractor, show=True):
        ext = extractor(root, name)
        self.bin_set = ext.extract(show=False)
        if show is True:
            print self.bin_set

    def __detail_callable(self, dcl):
        for box in dcl:
            cat = "__ca_"
            if cat in box:
                bci = box.index(cat)
                yield box[bci+len(cat):]

    def detail_list(self):
        return list(self.__detail_callable(dir(self)))

    def details(self, names=["accuracy"], show=True):
        self.__assert_set_data()
        dts = []
        for binn in self.bin_set:
            dt = dict()
            for name in names:
                dt[name] = self.detail(binn, name, show)
            dts.append(dt)
        return pd.DataFrame(dts)

    def detail(self, binn, name="accuracy", show=True):
        """
        binn: dictionary containing `tp`, `tn`, `fp`, `fn` keys
        """
        method = getattr(self, "_Accuracy__ca_{}".format(name))
        mv = method(**binn)
        if show is True:
            print "{}: {:5.3f}".format(name, mv)
        return mv

    def __data_not_set(self):
        return (not hasattr(self, "bin_set")) or \
            (self.bin_set is None) or (len(self.bin_set) == 0)

    def __assert_set_data(self):
        if self.__data_not_set():
            info = "Use set_data() before continue"
            print info
            raise Exception("Error", info)

    def __ca_accuracy(self, tp=0, fp=0, tn=0, fn=0):
        t = tp + tn
        a = t + fp + fn
        return t*1.0/a

    def __ca_precision(self, tp=0, fp=0, tn=0, fn=0):
        # positive predictive value (PPV)
        a = tp + fp
        return tp*1.0/a

    def __ca_npv(self, tp=0, fp=0, tn=0, fn=0):
        # negative predictive value (NPV)
        a = tn + fn
        return tn*1.0/a

    def __ca_sensitivity(self, tp=0, fp=0, tn=0, fn=0):
        # true positive rate (TPR, Recall, Hit-Rate)
        a = tp + fn
        return tp*1.0/a

    def __ca_speficity(self, tp=0, fp=0, tn=0, fn=0):
        # True Negative Rate (TNR)
        a = tn + fp
        return tn*1.0/a

    def __ca_fallout(self, tp=0, fp=0, tn=0, fn=0):
        # false positive rate (FPR)
        a = tn + fp
        return fp*1.0/a

    def __ca_fdr(self, tp=0, fp=0, tn=0, fn=0):
        # false discovery rate
        a = tp + fp
        return fp*1.0/a

    def __ca_fmeasure_raw(self, beta=1, tp=0, fp=0, tn=0, fn=0):
        p = self.precision(tp, fp, tn, fn)
        r = self.sensitivity(tp, fp, tn, fn)
        return self.fmeasure(beta, p, r)

    def fmeasure(self, beta=1, precision=0, recall=0):
        b2 = beta**2
        pr = precision*recall
        return (1+b2)*pr/(b2*precision+recall)

    def __ca_Emeasure_raw(self, beta=1, tp=0, fp=0, tn=0, fn=0):
        f = self.fmeasure_raw(beta, tp, fp, tn, fn)
        return 1-f

    def Emeasure(self, beta=1, precision=0, recall=0):
        f = self.fmeasure(beta, precision, recall)
        return 1-f
