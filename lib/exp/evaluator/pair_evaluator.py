import pandas as pd
import numpy as np
from sklearn import mixture
from base import Evaluator


class PairEvaluator(Evaluator):
    def __init__(self, pair_result, ground):
        """
        `matches`: Comes from matched result and containing keys as:
            `matches`, `sif`, `vif`
        `ground`: Ground-truths dataframe, columns are:
            'fid', 'sid', 'slide_type', 'cam_status'
        """
        self.pre = pair_result
        self.gnd = ground

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

    def __gmm_result(self, data, mm=2):
      clf = mixture.GMM(n_components=mm, covariance_type='full')
      clf.fit(data)
      pr = clf.predict(data)
      return np.array(self.__reorder(clf.means_.tolist(), pr))

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

    def __frame_gnd_tag(res, gnd):
        """
        Deprecated check_hist method
        """
        candi = []
        for di in res.index:
            qry = gnd[(gnd['fid'] <= di)]
            if len(qry) > 0:
                candi.append(qry.values[-1][1])
            else:
                candi.append(-1)
        res['ground_sid'] = candi

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
        hitd = pd.DataFrame(hita, columns=cols)
        hitd = hitd.set_index('fid')
        hitd['pair'] = self.__gmm_result(hitd.dist.values, 2)
        return hitd

    def hitd_praf(self, hitd):
        """
        Get the precision, recall, accuracy, fmeasure of results
        """
        hvr = [v[2] for v in hitd['vr'].values]
        g_slid = hvr > 0
        r_slid = hitd['sid'] == hvr
        tp = len(hitd[g_slid & r_slid])
        fp = len(hitd[g_slid & ~r_slid])
        tn = len(hitd[~g_slid & ~r_slid])
        fn = len(hitd[~g_slid & r_slid])
        return self.praf(tp, fp, tn, fn)

    def evaluation(self):
        pass
