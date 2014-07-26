# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

rks = ["lib.exp.summ"]
reload_mods(rks)

from lib.exp.summ import Mary
mm = Mary()

import warnings
warnings.filterwarnings('ignore')

# <codecell>

dc = mm.df_classify_perf()

# <codecell>

rks = ["lib.texer.sum_ns_tab", "lib.texer"]
reload_mods(rks)

from lib.texer import Texer
tex = Texer()
#print tex.sum_ns_roc(dc[:])

# <codecell>

rks = [
  "lib.plotter.ax_helper", "lib.plotter.plot_filer",
  "lib.plotter.summ.fig_plot", 
       "lib.plotter.summ"]
reload_mods(rks)

from lib.plotter.summ import MaryPlotter
mp = MaryPlotter()

# <codecell>

fig = plt.figure(figsize=(10, 5))
dc = mp.classfy_perf(fig=fig, ks=range(0, 2))
fig = plt.figure(figsize=(15.6, 5))
dc = mp.classfy_perf(fig=fig, ks=range(2, 5))

# <codecell>


# <codecell>

dc[dc.dsn!="coates"]

# <codecell>

reduce(lambda x, y: "{},{}".format(x, y), dc.index)

# <codecell>


