import matplotlib.cm as mcm


class _AccPlot(object):
    Markers = ["o", "x", "-", ">", "<", "0"]
    Colors  = mcm.Set1(range(len(Markers)))

    def __init__(self, preset_id=0):
        self.pid = preset_id

    def __plot_conf(self):
        m = self.Markers[self.pid]
        c = self.Colors[self.pid]
        return dict(marker=m, color=c)

    def __add_label(self, ax):
        ax.set_ylabel("Sensitivity", fontsize=14)
        ax.set_xlabel("Precision", fontsize=14)
        ax.set_title("Preprocessing ROC curve", fontsize=18, y=1.02)

    def plot(self, ax, data):
        conf = self.__plot_conf()
        data.plot(x="precision", y="sensitivity", ax=ax, **conf)
        self.__add_label(ax)
        for pi, pd in data.iterrows():
            x = pd.precision
            y = pd.sensitivity-.04
            ax.text(x, y, pd.key, ha='center', fontsize=14)
