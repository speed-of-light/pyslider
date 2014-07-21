class _RocGrid(object):
    def __init__(self, kname, cm):
        self._cm = cm
        self._kname = kname

    def __base_config(self, ax):
        ax.patch.set_visible(0)

    def __add_labels(self, ax, key):
        ax.set_title(key[:-4], fontsize=18)
        ax.set_xlabel("Precision", fontsize=14)
        ax.set_ylabel("Recall", fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    def __ntbase(self, ax, data, key):
        si = data[key].argmax()
        dk = data.ix[si]
        nt = "{}-{}".format(dk.name, dk["name"])
        ax.text(dk.precision, dk.sensitivity - .02, nt, ha="center", va="top")

    def __add_notable_text(self, ax, data):
        self.__ntbase(ax, data, "sensitivity")
        self.__ntbase(ax, data, "precision")

    def __kg_roc_plot(self, ax, key, data):
        self.__base_config(ax)
        data.plot(x="precision", y="sensitivity", ax=ax, color="r", ls="", marker="x")
        self.__add_labels(ax, key)
        self.__add_notable_text(ax, data)

    def plot(self, fig, data):
        ft = "{} Comparisons of ROC curve".format(self._kname)
        fig.suptitle(ft, fontsize=18, y=.92)
        for ei, (di, dg) in enumerate(data.groupby("key"), 1):
            ax = fig.add_subplot(6,3, ei)
            self.__kg_roc_plot(ax, di, dg)
