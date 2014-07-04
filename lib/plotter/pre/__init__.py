__doc__ = """
Preprocessing data result plotter
"""

__all__ = ["_base", "_exts"]

from base import _Base
from exts import _Exts


class PrePlotter(_Exts, _Base):
    def __init__(self):
        _Base.__init__(self)
        _Exts.__init__(self)

    def fc_delay_relations(self, ax, data, cols,
                           key="Delay-time vs Frame Difference"):
        """
        data: dataframe with columns `diff`, `dist`
        """
        hls = None
        if "diff" in cols:
            ax, hls = self.diff_plot(ax, data["diff"], hls)
        if "dist" in cols:
            ax, hls = self.dist_plot(ax, data["dist"], hls)
        ax.set_xlim(0, max(data.index))
        ax.legend(hls[0], hls[1], loc=0)
        ax.set_title(key, fontsize=18, y=1.03)
        return ax

    def batch_delay_relations(self, fig, root, name):
        """
        Usage:
            fig = plt.figure(figsize=(15, 38))
            ppt.batch_delay_relations(fig, *dn)
        """
        _Exts._reload_obj(self, root, name, "reducer")
        _Exts._reload_obj(self, root, name, "preproc")
        dzip = zip(range(len(self.names)), self.names, self.rkeys)
        for ri, na, rk in dzip:
            df = self._get_reduced_data(self.re_, rk, self.pp_)
            # plot
            ax = fig.add_subplot(len(self.names), 1, ri)
            title = "[Data: {}-{}] {}".format(root, name, na)
            self.fc_delay_relations(ax, df, cols=["diff", "dist"], key=title)
