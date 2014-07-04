class Accuracy(object):
    def __init__(self):
        pass

    def set_data(self, data, caller):
        bins = caller.call(data)
        return bins

    def accuracy(self, tp=0, fp=0, tn=0, fn=0):
        t = tp + tn
        a = t + fp + fn
        return t*1.0/a

    def precision(self, tp=0, fp=0, tn=0, fn=0):
        # positive predictive value (PPV)
        a = tp + fp
        return tp*1.0/a

    def npv(self, tp=0, fp=0, tn=0, fn=0):
        # negative predictive value (NPV)
        a = tn + fn
        return tn*1.0/a

    def sensitivity(self, tp=0, fp=0, tn=0, fn=0):
        # true positive rate (TPR, Recall, Hit-Rate)
        a = tp + fn
        return tp*1.0/a

    def speficity(self, tp=0, fp=0, tn=0, fn=0):
        # True Negative Rate (TNR)
        a = tn + fp
        return tn*1.0/a

    def fallout(self, tp=0, fp=0, tn=0, fn=0):
        # false positive rate (FPR)
        a = tn + fp
        return fp*1.0/a

    def fdr(self, tp=0, fp=0, tn=0, fn=0):
        # false discovery rate
        a = tp + fp
        return fp*1.0/a

    def fmeasure_raw(self, beta=1, tp=0, fp=0, tn=0, fn=0):
        p = self.precision(tp, fp, tn, fn)
        r = self.sensitivity(tp, fp, tn, fn)
        return self.fmeasure(beta, p, r)

    def fmeasure(self, beta=1, precision=0, recall=0):
        b2 = beta**2
        pr = precision*recall
        return (1+b2)*pr/(b2*precision+recall)

    def Emeasure_raw(self, beta=1, tp=0, fp=0, tn=0, fn=0):
        f = self.fmeasure_raw(beta, tp, fp, tn, fn)
        return 1-f

    def Emeasure(self, beta=1, precision=0, recall=0):
        f = self.fmeasure(beta, precision, recall)
        return 1-f
