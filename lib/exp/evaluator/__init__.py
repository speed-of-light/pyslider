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

    def praf(self, tp=0, fp=0, tn=0, fn=0):
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

    def __make_confusion(self, correct, sid, fid):
        con = dict(tp=0, tn=0, fp=0, fn=0, fid=fid, sid=sid)
        predict_with_sid = (sid > 0)
        predict_with_nosid = (sid == -1)
        if not correct and predict_with_nosid:
            con["fn"] = 1
        elif not correct and predict_with_sid:
            con["fp"] = 1
        elif correct and predict_with_nosid:
            con["tn"] = 1
        elif correct and predict_with_sid:
            con["tp"] = 1
        return con

    def __cfs_to_praf(self, cfs):
        prafd = dict(tp=0, tn=0, fp=0, fn=0)
        for cf in cfs:
            for fk in prafd.keys():
                prafd[fk] += cf[fk]
        return self.praf(**prafd)

    def __guess_to_praf(self, gnd, sid, fid):
        oc = gnd.guess(sid, fid)  # outcome
        cf = self.__make_confusion(oc, sid, fid)
        return cf

    def __wrongs(self, gnd, cfs):
        wg = []
        for ci, cf in enumerate(cfs):
            if (cf["fn"] == 1) or (cf["fp"] == 1):
                ans = gnd.answer(cf["fid"])
                wg.append(dict(ci=ci, ans=ans, fid=cf["fid"], sid=cf["sid"]))
        return wg

    def eval_sfps(self, gnd, sfps):
        """
        sfp: slide-frame pairs
        """
        cfs = []
        for sfp in sfps:
            cf = self.__guess_to_praf(gnd, *sfp)
            cfs.append(cf)
        praf = self.__cfs_to_praf(cfs)
        wrongs = self.__wrongs(gnd, cfs)
        print self.__praf_str(*praf)
        return praf, wrongs
