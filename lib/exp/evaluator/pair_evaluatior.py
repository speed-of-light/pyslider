import pandas as pd
import numpy as np
from sklearn import mixture


class PairEvaluator(object):
    def __init__(self, pair_result, ground):
        """
        `matches`: Comes from matched result and containing keys as:
            `matches`, `sif`, `vif`
        `ground`: Ground-truths dataframe, columns are:
            'fid', 'sid', 'slide_type', 'cam_status'
        """
        self.pre = pair_result
        self.gnd = ground

    def __gmm_result(self, data, mm=2):
      clf = mixture.GMM(n_components=mm, covariance_type='full')
      clf.fit(data)
      pr = clf.predict(data)
      return np.array(self._reorder(clf.means_.tolist(), pr))

    def __check_hits(self, fid, feats, votes):
        """
        Find a matched pair is right or wrong
        """
        last = -1
        _sid = 1  # column index of `sid` in gnd dataframe
        gnd = self.gnd
        ggd = gnd[(gnd['fid'] <= fid)]
        if len(ggd) > 0:
            sid = ggd.values[last][_sid]  # best matched sid in ground
            mr = feats[sid-1]['mr']  # matched result, since sid starts from 1
            f_one = mr.dt.quantile(.1)
            tmean = mr[mr.dt.lt(f_one)].dt.mean()
            if sid > 0:  # has sid in ggd, so possibly hit
                data = [fid, sid, votes, True, False, tmean]
            else:  # if len(mr) > 0: # has matched result but no hit
                data = [fid, sid, votes, False, True, tmean]
        else:
            print 'should never goes here'
        return data

    def pairing(self):
        """
        Generate the pair result with `hit` and `non-hit` marks
        Returned cols:
            `fid`, `sid`, `vr`, `dist`, `pair`
        """
        hita = []
        pres = self.pre
        for r in pres:
            pfeats = r['feats']
            fid = pfeats[0]['fid']  # 0 is ok, all the same
            hita.append(self.__check_hits(fid, pfeats, r['vr']))
        cols = ['fid', 'sid', 'vr', 'dist']
        hitf = pd.DataFrame(hita, columns=cols)
        hitf = hitf.set_index('fid')
        hitf['pair'] = self.__gmm_result(hitf.dist.values, 2)
        return hitf
