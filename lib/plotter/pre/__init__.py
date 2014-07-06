__doc__ = """
Preprocessing data result plotter
"""

__all__ = []

from functools import wraps  # enables @wraps
from base import _Base as Base
from exts import _Exts as Exts
from lib.plotter.plot_filer import _PlotFiler as PF
from rtplot import _RtPlot as RP
from acc_plot import _AccPlot as AP
from cov_plot import _CovPlot as CovP
from frames_plot import _FramesPlot as FrmP
from delay_plot import _DelayPlot as DeP


class PrePlotter(Exts, Base, PF):
    def __init__(self, autosave=False):
        PF.__init__(self)
        Base.__init__(self)
        Exts.__init__(self)
        self.autosave_fig = autosave

    def render_base(func):
        @wraps(func)  # enable func.__name__
        def inner(self, *args, **kwargs):
            Base._assert_rootname_exist(self)
            Base._common_axes(self, kwargs["fig"])
            data = func(self, *args, **kwargs)
            PF._savefig(self, kwargs["fig"], func.__name__, self.rn)
            return data
        return inner

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

    @render_base
    def batch_delay_relations(self, fig):
        """
        Usage:
            fig = plt.figure(figsize=(15, 38))
            ppt.set_rootname(ro, na)
            ppt.batch_delay_relations(fig, *dn)
        """
        for ri, na, rk, dof in Base._name_key_zip(self):
            df = self._get_reduced_slides(rk, dof)
            # plot
            ax = fig.add_subplot(len(self.names), 1, ri+1)
            ax.patch.set_alpha(0.0)
            title = Base._title_tag(self, na)
            self.fc_delay_relations(ax, df, cols=["diff", "dist"], key=title)

    @render_base
    def fc_cov_comparisons(self, fig=None):
        kz = Base._name_key_zip(self)
        data = Exts._get_slide_coverages(self, kz)
        print data
        pt = CovP(self.rootname)
        pt.plot(fig.axes[0], data)

    @render_base
    def batch_frame_ratio(self, fig=None):
        """
        Compare frame reduced ratio based on rootname
        """
        Exts._reload_obj(self, "reducer")
        rp = RP(self.re_)
        rp.frame_reduced_ratio(fig.axes[0])

    @render_base
    def roc_curve(self, fig=None):
        data = Exts._get_accuracy(self)
        ap = AP(0)
        ap.plot(fig.axes[0], data)
        return data

    @render_base
    def frame_list(self, fig=None, key="", seeds=[], all_seg=False,
                   rand=False, lim=54):
        # Print out of most `len(seeds) + lim` frames
        rdf = self._get_reduced_segments(key)
        fp = FrmP(self.root, self.name)
        fp.set_data(rdf, seeds=seeds, all_seg=all_seg, rand=rand, lim=lim)
        title = "{} \nRandom Selected Candidate Frames".format(self.rootname)
        fp.plot(fig, title)
