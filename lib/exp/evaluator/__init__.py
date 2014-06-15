__all__ = ['ground_truth']
from ground_truth import GroundTruth


class Evaluator(object):
    def __init__(self):
        pass

    def fbeta(self, precision, recall, beta=1):
        """
        F1: for bata = 0.5, also called f1 score
        F2: for bata = 1
        """
        return (1+beta**2)*precision*recall/((beta**2)*precision+recall)

    def praf(self, tp, fp, tn, fn):
        precision = tp*1.0/(tp+fp)
        recall = tp*1.0/(tp+fn)
        accuracy = (tp+tn)*1.0/(tp+tn+fp+fn)
        fmeasure = self.fbeta(precision, recall, .5)
        # print self.__praf_str(precision, recall, accuracy, fmeasure)
        return (precision, recall, accuracy, fmeasure)

    def __praf_str(self, p, r, a, f):
        aa = []
        aa.append("Precision: {:.3f}".format(p))
        aa.append("Recall: {:.3f}".format(r))
        aa.append("Accuracy: {:.3f}".format(a))
        aa.append("Fmeasure: {:.3f}".format(f))
        ast = ""
        for a_ in aa:
            ast += "{}\n".format(a_)
        return ast

    def __keg_pack(self, gnd, tar):
        raw = gnd.univ_df()
        keg = dict()
        keg["info"] = gnd.info()
        if "absp" in tar:
            keg["absp"] = raw[raw.sid > 0]
        if "relp" in tar:
            keg["relp"] = gnd.shrink(raw[raw.sid > 0])
        if "seg" in tar:
            keg["seg"] = gnd.segments(raw, 'duration')
        return keg

    def pack_gnd(self, roots, names, targets):
        """
        `roots`: dataset roots
        `names`: dataset names, paired with roots
        `targets`: list with data format currently support:
            `absp`: for `absolute pairs`
            `relp`: for `relative pairs`
            `seg`: for `segments` (**buggy**)
        Return packed dict data by named keys
        """
        keg = {}
        for root, name in zip(roots, names):
            gt = GroundTruth(root, name)
            ns = root + "_" + name
            keg[ns] = self.__keg_pack(gt, targets)
        return keg
