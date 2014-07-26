class _RocPlot(object):
    def __init__(self, dskey, cm, marker):
        self._dskey = dskey
        self._cm = cm
        self._marker = marker

    def __ax_annotation(self, ax):
        dsk = self._dskey
        ids = "{} Slide-Frame detection ROC curve".format(dsk)
        ax.set_xlabel("Speficity", fontsize=14)
        ax.set_ylabel("Sensitivity", fontsize=14)
        ax.set_title(ids, fontsize=14)
        leg = ax.legend(loc=0)
        leg.get_frame().set_alpha(0.7)

    def __adjust_ax(self, ax):
        ax.patch.set_visible(False)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    def __plot_annotation(self, ax, data, xs, ys, cpn):
        xy = (data[xs], data[ys])
        arp = dict(width=.0, headwidth=.0, frac=.2,
                   shrink=.2, linewidth=0, color='b')
        ax.annotate(data[cpn], xy=xy, xytext=(xy[0]*.99, xy[1]*.95),
                    fontsize=12, ha="right", va="bottom", arrowprops=arp)

    def __plot_core(self, ax, ei, gi, gd, cpn="name"):
        mk, clr = self._marker[ei % 4], self._cm(ei*1.0/self._cm.N)
        xs, ys = "speficity", "sensitivity"
        gd.plot(x=xs, y=ys, marker=mk, markersize=11, ls="-",
                color=clr, ax=ax, label=gi)
        pam = lambda data: self.__plot_annotation(ax, data, xs, ys, cpn)
        [pam(grd) for gri, grd in gd.iterrows()]

    def plot(self, ax, data, compare=["key", "name"]):
        self.__adjust_ax(ax)
        xgg = data.groupby(compare[0])
        self._cm.N = len(xgg)
        pcm = lambda e, g, d: self.__plot_core(ax, e, g, d, compare[1])
        [pcm(ei, gi, gd) for ei, (gi, gd) in enumerate(xgg, 0)]
        self.__ax_annotation(ax)
