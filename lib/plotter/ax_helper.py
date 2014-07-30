class AxHelper(object):
    def __init__(self):
        pass

    def _ax_hide_patch_spines(self, ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.itervalues():
            sp.set_visible(False)

    def _ax_hide_xy_axis(self, ax):
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    def _ax_hide_patch_spine_axis(self, ax):
        self._ax_hide_patch_spines(ax)
        self._ax_hide_xy_axis(ax)

    def _ax_shift_yaxis(self, ax, spine_pos="right", delta=1.1):
        ax.spines[spine_pos].set_position(("axes", delta))
        self._ax_hide_patch_spines(ax)
        ax.spines[spine_pos].set_visible(True)

    def _ax_hide_ticks(self, ax):
        ax.set_xticks([])
        ax.set_yticks([])

    def _ax_transparent(self, ax):
        ax.patch.set_visible(False)
