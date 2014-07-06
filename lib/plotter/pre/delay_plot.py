from lib.exp.pre import Const
from lib.plotter.ax_helper import AxHelper


class _DelayPlot(AxHelper):
    def __init__(self, data):
        self.data = data

    def plot(self, fig):
        for dt in self.data:
            ax = fig.add_subplot(len(self.names), 1, ri+1)
            ax.patch.set_alpha(0.0)
            title = Base._title_tag(self, na)
            self.fc_delay_relations(ax, df, cols=["diff", "dist"], key=title)
