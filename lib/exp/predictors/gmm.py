from sklearn import mixture
from base import Predictor


class GmmPredictor(Predictor):
    def __init__(self, fids, matches):
        Predictor.__init__(self, fids, matches)

    def __reorder(self, old, li=[]):
        """
        Generate reordered list by sorted old list values
        ex:
          old= [9,3,6]; li = [1,0,0,0,0,2,0,1]
          by product: bb = { 0: 1, 1:2, 2:0}
          return: [2, 1, 1, 1, 1, 0, 1, 2]
        """
        tmp = old[:]
        tmp.sort()
        bb = {}
        for i, t in enumerate(tmp):
            bb[i] = old.index(t)
        return [bb[ll] for ll in li]

    def __refit_non_slides(self, pr, data, mean):
        for di, d in enumerate(data):
            if d > mean:
                pr[di] = 1  # type of non slide
        return pr

    def __predict_core(self, data, nc=2):
        """
        Predict with `slide`, and `non-slide` 2 types
        """
        clf = mixture.GMM(n_components=nc, covariance_type='full')
        clf.fit(data)
        pr = clf.predict(data)
        pr = self.__reorder(clf.means_.tolist(), pr)
        pr = self.__refit_non_slides(pr, data, max(clf.means_))
        self.clf = clf
        return pr

    def __merge_raw_class(self, gsids, prclass):
        """
        Generate pure slide id predicted results
        """
        rpr = []
        for pi, p in enumerate(prclass):
            if p == 0:
                rpr.append(gsids[pi])
            elif p == 1:
                rpr.append(-1)
        return rpr

    def __means(self):
        mcs = self.matches
        return [sum(mc)/len(mc) for mc in mcs]

    def __slide_index(self):
        """
        Find slide id by minimun in matched distance
        Return guessed slide ids
        """
        mcs = self.matches
        gsids = []
        for mc in mcs:
            mlen = len(mc)
            guess_sid = min(xrange(mlen), key=mc.__getitem__)
            gsids.append(guess_sid+1)
        return gsids

    def __replace_no_feats_pairs(self, means, pr):
        for mi, mean in enumerate(means):
            if mean < 0:
                pr[mi] = -1
        return pr

    def predict(self):
        means = self.__means()
        gsids = self.__slide_index()
        pr = self.__predict_core(means)
        pr = self.__merge_raw_class(gsids, pr)
        pr = self.__replace_no_feats_pairs(means, pr)
        return zip(pr, self.fids)
