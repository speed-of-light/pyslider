import numpy as np
import inflection as Inf


class _Mater(object):
    obs = np.array(["mean_dist", "rdist", "inv_rdist",
                    "top50", "area_ratio"])
    def __init__(self, ks, ns, obk=[0,1,2,3,4]):
        self.ks = ks
        self.obs = self.obs[obk]
        self.csize = 200
        self.ns = ns

    def __finfo(self, ax, key):
        title = Inf.titleize(key)
        ax.set_title(title, fontsize=20)
        ax.set_xlabel("Candidate ID", fontsize=14)
        ax.set_ylabel("Slide ID", fontsize=14)
        ax.get_xaxis().tick_bottom()

    def __ratio_bar(self, cbar):
        labels = ["{:.1f}".format(ns) for ns in np.arange(.02, 1., .12)]
        loc = np.arange(.02, 1., 0.12)
        cbar.set_ticks(loc)
        labels[0], labels[-1] = "< 0.1", "> 0.9"
        cbar.set_ticklabels(labels)

    def __ax_mat(self, fig, ax, mat, vmax=None, st=0):
        cax = ax.matshow(mat, vmax=vmax, extent=(0, 200,1,48))
        cb = fig.colorbar(cax, fraction=.012, pad=.01)
        if vmax is not None:
            self.__ratio_bar(cb)
        ax.set_xticks(range(0, 200, 200/8))
        ax.set_xticklabels(range(st, st+201, 200/8))

    def __add_mat(self, fig, data, key, mi=1, st=0):
        ax = fig.add_subplot(len(self.obs), 1, mi)
        gcl = len(data.groupby("fid"))
        mat = data[key].reshape(gcl, self.ns).T[:, st:st+self.csize]
        vm = 1.2 if "area" in key else None
        self.__ax_mat(fig, ax, mat, vmax=vm, st=st)
        self.__finfo(ax, key)

    def plot(self, fig, df, st=0):
        fts = "Similarity Comparison {}".format(self.ks)
        fig.suptitle(fts, fontsize=23, y=.98)
        pltr = lambda i, k: self.__add_mat(fig, df, k, i, st=st)
        map(pltr, range(1, len(self.obs)+1), self.obs)
