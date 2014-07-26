# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

rks = [
  "lib.exp.summ.storage",
  "lib.exp.summ"]
reload_mods(rks)

from lib.exp.summ import Mary
mm = Mary()

import warnings
warnings.filterwarnings('ignore')

# <codecell>

#dc = mm.df_classify_perf(key="coverages_9")
#saf = mm.df_rec_ans()
sd = mm.get_storage()
sd.Classifier = [0, 1, 2]
sd.Reducer = [170, 167, 178]
sd.Feats = [1282, 1322, 1621]
sd.Slides = [40, 38, 42]
sd.Matches = [2265, 2695, 3105]
sd

# <codecell>

fig = plt.figure(figsize=(18, 5))
#fig.suptitle("Storage Comparisons of 3 dataset(MB)", fontsize=20, y=1.02)
kcrs = ["#3355ee", "#ee5533", "#449b44"]
crs = mpl.cm.GnBu(range(30,250, 30))
lbs = filter(lambda k: "dsn" not in k, sd.columns)
explode=(0, 0.1, 0, 0)
for si, sr in sd.iterrows():
  ax = plt.subplot(1, 3, si+1)
  dt = sr[lbs]
  dts = dt.sum()
  exp = (dt.values / (1.*dts))*.2
  pa, tx, txa = ax.pie(dt, explode=exp, labels=lbs, autopct='%1.1f%%', colors=crs)
  # texts
  [t.set_text(t.get_text() + "({})".format(v)) for t, v in zip(tx, dt.values)]
  [t.set_text("") for t, v in zip(tx, dt.values) if v == 0]
  [t.set_color(kcrs[si]) for t, v in zip(tx, dt.values)]
  [t.set_size(18) for t in tx]
  [t.set_size(18) for t in txa]
  # final
  ax.set_title("{} ({})".format(sr.dsn, dts), fontsize=32, color=kcrs[si])
fig.savefig("data/fig/mary/storage.eps", transparent=1)
#sd.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=270, fontsize=17)

# <codecell>

rks = ["lib.texer.sum_ns_tab", "lib.texer.sum_sf_cov", 
       "lib.texer"]
reload_mods(rks)

from lib.texer import Texer
tex = Texer()
#print tex.sum_ns_roc(dc[:])
#print tex.sum_ns_cov(dc)
print tex.sum_sf_cov(dc)

# <codecell>

rks = [
  "lib.plotter.ax_helper", "lib.plotter.plot_filer",
  "lib.plotter.xframes.rec_plot",
  "lib.plotter.summ.fig_plot", 
       "lib.plotter.summ"]
reload_mods(rks)

from lib.plotter.summ import MaryPlotter
mp = MaryPlotter()

# <codecell>

#fig = plt.figure(figsize=(10, 5))
#dc = mp.classfy_perf(fig=fig, ks=range(0, 2))
#fig = plt.figure(figsize=(15.6, 5))
#dc = mp.classfy_perf(fig=fig, ks=range(2, 5))
#fig = plt.figure(figsize=(18, 9))
#mp.rec_timeline(fig=fig, ds=[0], ks=[0,5])

# <codecell>

cc = mm.df_classify_perf(key="coverages_9")

# <codecell>

%debug

# <codecell>

fig = plt.figure(figsize=(18, 5))
fig.suptitle("Switch Coverages VS Confidence", fontsize=18, y=.99)
for ci, rg in cc.groupby("dsn"):
  ax = fig.add_subplot(1, 3, len(fig.axes)+1)
  ax.patch.set_visible(False)
  #print cg.sensitivity
  cg = rg.sort(columns=["fswc"])
  #print cg.key.values
  ax.plot(cg.fswc, color='r', marker='x', label="Switch Cov.")
  ax.plot(cg.tpc, color='g', marker='x', label="TP Confidence")
  ax.plot(cg.tnc, color='b', marker='x', label="TN Confidence")
  ax.set_title(ci.capitalize(), fontsize=16)
  ax.set_ylim(0,1)
  leg = ax.legend(loc=0, ncol=2)
  leg.get_frame().set_alpha(.2)
  tic, tap = -1, -1
  ax.set_xlabel("Methods", fontsize=14)
  ax.set_ylabel("Switch Coverage Rate", fontsize=14)
  for ei, (gi, gd) in enumerate(cg.iterrows()):
    if gd.key not in ['v_a_ans', 'v_atm_re_ans', 'v_atmri_ans']:
      continue
    #print gd
    ax.annotate(gd.key[:-4],
                xy=(ei, gd.fswc),  
                xytext=(ei, gd.fswc + gi*0.01*tic),   # theta, radius
                xycoords='data',
                textcoords='data',
                fontsize=14,
                arrowprops=dict(width=.5, frac=.15, shrink=.9, headwidth=5),
                ha='center', va='bottom',
                clip_on=False, # clip to the axes bounding box
     )
fig.savefig("data/fig/mary/soc.eps", transparent=1)

# <codecell>

fig.savefig("data/fig/mary/soc.eps", transparent=1)

# <codecell>

for ci, rg in cc.groupby("dsn"):
  print rg.sort(columns=["fslc", "fswc", "slc", "swc", "slcn", "swcn"], ascending=False)[:5]

# <codecell>

aa = [1,2]
[4] + aa

# <codecell>


