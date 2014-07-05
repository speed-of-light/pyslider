__doc__ = """
Preprocessing data result plotter
"""

__all__ = ["_base", "_exts"]

from base import _Base
from exts import _Exts
from rtplot import _RtPlot as RP


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
        _Base.set_rootname(self, root, name)
        for ri, na, rk in _Base._name_key_zip(self):
            df = self._get_reduced_data(self.re_, rk, self.pp_)
            # plot
            ax = fig.add_subplot(len(self.names), 1, ri+1)
            title = _Base._title_tag(self, na)
            self.fc_delay_relations(ax, df, cols=["diff", "dist"], key=title)

    def shr_sc_comparisons(self, fig):
        if _Base.rootname_not_set(self):
            print "set_rootname() before calling this function"
            return None
        kz = _Base._name_key_zip(self)
        pdf = _Exts._get_slide_coverages(self, self.root, self.name, kz)
        ax = fig.add_subplot(111)
        ax = pdf.plot(kind='bar', ax=ax)
        _Base._shr_sc_cp_labs(self, ax)
        _Base._shr_sc_texts(self, ax, pdf)

    def batch_frame_ratio(self, fig, root, name):
        """
        Compare frame reduced ratio based on rootname
        """
        _Exts._reload_obj(self, root, name, "reducer")
        rp = RP(self.re_)
        ax = fig.add_subplot(111)
        rp.frame_reduced_ratio(ax, self.names)

    def debug(self):
        kz = _Base._name_key_zip(self)
        pdf = _Exts._get_slide_coverages(self, self.root, self.name, kz)
        return pdf
