import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as mmlab


class MatchingHistPlotter(object):
    def __init__(self):
        self.bins = 100
        pass

    def hist_base(self, ax, clf, dists):
        (n, bins, patches) = plt.hist(dists, bins=self.bins, normed=True)
        colors = ['red', 'limegreen', 'skyblue']
        gpcm = clf.means_
        grng = range(len(gpcm))
        for i, m, w, c in zip(grng, gpcm, clf.weights_, clf.covars_):
            ax.plot(bins, w*mmlab.normpdf(bins, m, np.sqrt(c))[0],
                    lw=2, color=colors[i])
            ax.axvline(x=m, color=colors[i], lw=2)
        return n, bins

    def __nval_from_bins(self, key, nval, bins):
        for bi, b in enumerate(bins):
            if key < b:
                break
        return nval[bi-1]

    def __xypos(self, thres, x, wi):
        va = 1 if x > thres else 0.1
        return va

    def wrong_mark(self, ax, wrongs, clf, dists):
        (nval, bins, p) = plt.hist(dists, bins=self.bins, normed=True)
        for wi, w in enumerate(wrongs):
            pair_str = "f#{fid}-s#{sid}".format(**w)
            wci = w["ci"]
            nbv = self.__nval_from_bins(dists[wci], nval, bins)
            cf = clf.means_[0][0]
            x = self.__xypos(cf, dists[wci], wi)
            ax.annotate(
                pair_str, xy=(dists[wci], nbv),
                xytext=(x, 1-((wi*2.0/len(wrongs) % 1))),
                xycoords="data", textcoords='axes fraction',
                arrowprops=dict(arrowstyle="->", color='#5566EE'))
