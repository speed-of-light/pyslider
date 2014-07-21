import pandas as pd
import numpy as np
from sklearn import mixture


class _Core(object):
    def __init__(self):
        pass

    def __reorder(self, old, li=[]):
        """
        Generate reordered list by sorted old list values
        ex:
          old= [9,3,6]; li = [1,0,0,0,0,2,0,1]
          by product: bb = { 0: 1, 1:2, 2:0}
          return: [2, 1, 1, 1, 1, 0, 1, 2]
        """
        tmp = old[:]
        tmp.sort()  # 1,2,3
        bb = {}
        for i, t in enumerate(tmp):
            bb[i] = old.index(t)
        return np.array([bb[ll] for ll in li])

    def __gmmize(self, data):
        clf = mixture.GMM(n_components=self.gmmc, covariance_type='full')
        clf.fit(data)
        pr = clf.predict(data)
        means = clf.means_.tolist()
        return self.__post_tuning(data.values, pr, means)

    def __post_tuning(self, base, predicted, means):
        """
        Manual change dist over no_slides, and below hs_slides
        """
        means = [m[0] for m in means]
        ret = self.__reorder(means, predicted)
        ret[base >= np.max(means)] = 1
        ret[base <= np.min(means)] = 0
        return ret

    def __area_swap(self, data, gre):
        # gre[gre == 0] = 2
        # gre[gre == 1] = 0
        # gre[gre == 2] = 1
        gr = np.array([1] * len(gre))
        gr[gre.values > 0.1999] = 0
        return gr

    def _gmm_base(self, data, key="mean", post="_dist"):
        tn = data["{}{}".format(key, post)]
        if len(tn) == len(tn[tn.isnull()]):
            gr = [1] * len(tn)
        else:
            if "area" in key:
                gr = self.__area_swap(data,tn)
            else:
                gr = self.__gmmize(tn)
        data["{}_ans".format(key)] = gr

    def _gmm(self, data, keys=["mean"], post="_dist"):
        for ky in keys:
            self._gmm_base(data, ky, post)
