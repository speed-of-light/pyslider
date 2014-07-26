import numpy as np
from lib.plotter.ax_helper import AxHelper


class FigPlot(AxHelper):
    def __init__(self, db):
        self.db = db

    _mark = ["x", "o", "^"]
    _clrs = ["r", "#55FE8b", "#6677EF"]
    _skey = np.array(["Bot Area Ans", "Top50 Ans", "Mean Ans", "Ridist Ans", "Rdist Ans"])

    def __concat_data(self):
        dp = None
        for df in self.db:
            dff = df[df.key.isin(self._skey)]
            dp = dff if dp is None else dp.append(dff)
        return dp

    def __ax_info(self, ax, fk):
        ax.set_title(fk, fontsize=16)
        ax.set_xlabel("$1-Speficity$", fontsize=16)
        ax.set_ylabel("$Sensitivity$", fontsize=16)

    def __base_item(self, ax):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        self._ax_transparent(ax)

    def __plot_data(self, ax, df, key):
        dft = df[df["key"] == key].sort(columns=[ "speficity", "sensitivity"], ascending=False)
        for ei, (di, dg) in enumerate(dft.groupby("dsn")):
            ax.plot(1- dg.speficity, dg.sensitivity, label=dg.iloc[0]["dsn"],
                    ls="-", color=self._clrs[ei], marker=self._mark[ei])
        ax.legend(loc=0)
        return dft

    def __annotate(self, ax, df):
        tap, kap = 1, -1
        for ri, rr in df[(df.sensitivity > 0.90) & (df.speficity > 0.9)].iterrows():
            tap = kap * tap
            ax.text((1-rr.speficity)+.001*ri*tap, rr.sensitivity+.001*ri*tap, rr["name"])

    def __plot(self, fig, df, fk, fsc):
        ax = fig.add_subplot(1, fsc, len(fig.axes)+1)
        self.__base_item(ax)
        dft = self.__plot_data(ax, df, fk)
        self.__ax_info(ax, fk)
        self.__annotate(ax, dft)

    def _classfy_roc(self, fig, ks=[0, 1]):
        df = self.__concat_data()
        pt = lambda fk: self.__plot(fig, df, fk, len(ks))
        map(pt, self._skey[ks])
