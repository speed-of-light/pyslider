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
        return [bb[ll] for ll in li]

    def __gmmize(self, data):
        clf = mixture.GMM(n_components=self.gmmc, covariance_type='full')
        clf.fit(data)
        pr = clf.predict(data)
        return np.array(self.__reorder(clf.means_.tolist(), pr))

    def _gmm_base(self, data, key="mean_dist"):
        tn = data[key]
        kn = key.split("_")[0]
        data["{}_ans".format(kn)] = self.__gmmize(tn)

    def _gmm(self, data, keys=["mean_dist"]):
        for ky in keys:
            self._gmm_base(data, ky)
