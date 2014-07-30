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
if False:
  sd = mm.get_storage()
  sd.Classifier = [0, 1, 2]
  sd.Preprocess = [170, 167, 178]
  sd.Features = [1282, 1322, 1621]
  sd.Slides = [40, 38, 42]
  sd.Matches = [97, 93, 67]
  mm.save("storage", sd)
  sd = sd.sort(columns=["dsn"])
  sd

# <codecell>

fig = plt.figure(figsize=(18, 5))
#fig.suptitle("Storage Comparisons of 3 dataset(MB)", fontsize=20, y=1.02)
kcrs = ["#335588", "#975533", "#448b35"]
crs = mpl.cm.GnBu(range(30,250, 30))
lbs = filter(lambda k: "dsn" not in k, sd.columns)
explode=(0, 0.1, 0, 0)
for ei, (si, sr) in enumerate(sd.iterrows(), 1):
  ax = plt.subplot(1, 3, ei)
  dt = sr[lbs]
  dts = dt.sum()
  exp = (dt.values / (1.*dts))*.2
  pa, tx, txa = ax.pie(dt, explode=exp, labels=lbs, autopct='%1.1f%%', colors=crs, startangle=110)
  # texts
  [t.set_text(t.get_text() + "({})".format(v)) for t, v in zip(tx, dt.values)]
  [t.set_text("") for t, v in zip(tx, dt.values) if v == 0]
  [t.set_color(kcrs[si]) for t, v in zip(tx, dt.values)]
  [t.set_size(18) for t in tx]
  [t.set_size(18) for t in txa]
  #[t.set_color(kcrs[si]) for t in txa]
  # final
  ax.set_title("{} ({})".format(sr.dsn, dts), fontsize=32, color=kcrs[si])
fig.savefig("data/fig/mary/storage.eps", transparent=1)

# <codecell>

rks = ["lib.texer.sum_ns_tab", "lib.texer.sum_sf_cov", 
       "lib.texer"]
reload_mods(rks)

from lib.texer import Texer
tex = Texer()
#print tex.sum_ns_roc(dc[:])
#print tex.sum_ns_cov(dc)
#print tex.sum_sf_cov(dc, cov=False)

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

from lib.exp.featx import Featx
fx = Featx("univ_07", "coates")
from lib.exp.pairing import PairFeats
pf = PairFeats(fx)
df = fx.load("rtlog")
df = df.drop_duplicates(cols=["key"])
print df.time.sum()
pf.set_matcher()
pf._update_klass_var()
df = pf.load("rs_d80_ra1000_rm10_iw0_ot0_NoHomo_Area")
print df.time.sum()

# <codecell>

td = pd.DataFrame(columns=sd.columns)
for sc in sd.columns:
  td[sc] = [0,0,0]
td.Features = [154034.75189208984, 40080.8579922, 190572.567463]
td["Matches"] = [1496278.0277729034, 343546.187878, 1121270.24841]
td["dsn"] = sd.dsn

# <codecell>

def to_mins(ms):
  tsec = ms / 1000
  sec = tsec % 60
  tmins= int(tsec / 60)
  mins = tmins % 60
  hr = int(tmins / 60)
  return "{:02d}:{:02d}:{:02.0f}".format(hr, mins, sec)

def time_pie(fig, df, cols=["Features", "Matches"], fn="time"):
  kcrs = ["#335588", "#975533", "#448b35"]
  crs = mpl.cm.Pastel2(range(120,250, 50))
  explode=(0, 0.1, 0, 0)
  for ei, (si, sr) in enumerate(df.iterrows(), 1):
    ax = plt.subplot(1, 3, ei)
    dt = sr[cols]
    dts = dt.sum()
    exp = (dt.values / (1.*dts))*.2
    pa, tx, txa = ax.pie(dt, explode=exp, labels=cols, autopct='%1.1f%%', colors=crs)
    # texts
    [a.set_text(a.get_text() + "\n" + t.get_text() + "({})".format(to_mins(v))) for a, t, v in zip(txa, tx, dt.values)]
    [t.set_text("") for a, t, v in zip(txa, tx, dt.values)]
    [t.set_color(kcrs[si]) for t, v in zip(txa, dt.values)]
    [t.set_size(18) for t in txa]
    # final
    ax.set_title("{} ({})".format(sr.dsn, to_mins(dts)), fontsize=32, color=kcrs[si])
  fig.savefig("data/fig/mary/{}.eps".format(fn), transparent=1)
  
fig = plt.figure(figsize=(18, 5))
time_pie(fig, td)

# <codecell>

td = td.sort(columns=["dsn"])

# <codecell>

ftd = td[:]
ftd["prer"] = [0.0087, 0.0089, 0.0050]

# <codecell>

ftd["All_Features"] = ftd.Features/ftd.prer
ftd["All_Matching"] = ftd.Matches/ftd.prer
#print ftd
fig = plt.figure(figsize=(18, 5))
time_pie(fig, ftd, cols=["All_Features", "All_Matching"], fn="exp_time")

# <codecell>

from lib.exp.summary import Summary
su = Summary()
sud = su.load_summary()

# <codecell>

fmts = dict(Time=to_mins)

sud = sud[sud.n_name.isin(["chaves", "coates", "rozenblit"])]
fcc = ["n_name", "n_frames", "n_slides", "n_time", "v_width", "v_height"]
sdd = sud[fcc]
sdd.columns = [fc[2:].capitalize() for fc in fcc]
sdd.Time = sdd.Time * 1000
sdd["Difficulty"] = ["Mixed background, Animated Slides", "Simpler background, Plain slides", "Lots similar, image slides"]

# <codecell>

print sdd.to_latex(index=0, formatters=fmts)

# <codecell>

cpf = pd.DataFrame(columns=["Critirions", "Proposed", "Fan_11"])
cpf = cpf.append([dict(Critirions="Time($GLOB+LOC$)", Proposed="00:16:27", Fan_11="00:38:40")])
cpf = cpf.append([dict(Critirions="Global Time($GLOB^1$)", Proposed="39:59:14", Fan_11="09:36:24")])
cpf = cpf.append([dict(Critirions="Avg. Accuracy($1-FER^2$)", Proposed="52%", Fan_11="98.2%")])
cpf = cpf.append([dict(Critirions="Best Switch Coverages($1-SER^3$)", Proposed="96.7%", Fan_11="94.4%~98.3%")])
cpf = cpf.append([dict(Critirions="Worst Switch Coverages($1-SER^3$)", Proposed="96.7%", Fan_11="94.4%~98.3%")])
print cpf.to_latex(index=0)

# <codecell>

print to_mins(ftd.Features.mean())
print to_mins(ftd.Matches.mean())
print to_mins(ftd.All_Features.mean())
print to_mins(ftd.All_Matching.mean())

# <codecell>

def bold_negative(v):
  if v == -1:
    return "STextbfBFSTextcolorBFemphasisBRBF-1BRBR"
  else:
    return "{}".format(v)

def cp(v):
  if v < 1.00:
    return "STextitBFSTextcolorBFemphasisBRBF{:4.1f}%BRBR".format(v*100)
  else:
    return "{:4.1f}%".format(v*100)

#seeds = saf.iloc[randint(0, high=len(saf), size=10)]
fsc = ["fid", "gnd", "area", "top50", "mean", "rmean", "invr"]
fsc = ["fid", "gnd", "v_a_ans", "v_at_ans", "v_atm_ans", "v_atmri_ans", "v_atm_re_ans"]
fsc = ["fid", "gnd", "v_a_conf", "v_at_conf", "v_atm_conf", "v_atmri_conf", "v_atm_re_conf"]
fsd = seeds[fsc].sort(columns=["fid"])
fsd.columns = [f.capitalize() for f in fsd.columns]
bn = bold_negative
#V_at_conf=bn, V_atm_ans=bn, V_atmri_ans=bn)).
print fsd.to_latex(index=0,  formatters=dict(
  Gnd=bn, V_a_conf=cp, V_at_conf=cp, V_atm_conf=cp, V_atmri_conf=cp, V_atm_re_conf=cp), float_format="{:.2f}".format). \
  replace("ST", "\\t").replace("BF", "{").replace("BR", "}").replace("V\\_", "").\
  replace("\_ans", "")

# <codecell>

seeds

# <codecell>

from lib.exp.tools.video import Video
from lib.exp.tools.slider import Slider
from lib.exp.featx import Featx

dn = ("univ_07", "coates")
vid = Video(*dn)
slr = Slider(*dn)
fx = Featx(*dn)
fid, sid = 18050, 16
sp = fx.load("s_{:03d}_kps".format(sid))
fp = fx.load("f_{}_kps".format(fid))
vimg = vid.get_frames(ids=[fid]).next()["img"]
simg = slr.get_slides(ids=[sid], resize=(vimg.shape[1], vimg.shape[0])).next()["img"]

# <codecell>

def draw_kps(ax, img, kps, show=1, ty="Frame", iid=18050):
  ax.imshow(img[:, :, [2, 1, 0]])
  if show:
    ax.scatter(kps.x, kps.y, marker="x", color="#55Fe36")
    ax.scatter(kps.x, kps.y, marker=".", facecolors="none", edgecolors="#EE5869", s=kps.size*50)
  ax.set_xlim(0, img.shape[1])
  ax.set_ylim(img.shape[0], 0)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_title("{}[{}]".format(ty, iid), fontsize=16)

fig = plt.figure(figsize=(18, 6))
ax = fig.add_subplot(122)
draw_kps(ax, vimg, fp, show=1, iid=fid)
ax = fig.add_subplot(121)
draw_kps(ax, simg, sp, show=1, ty="Slide", iid=sid)
fig.savefig("data/fig/mary/sift_after.eps", transparent=1)

# <codecell>

fp.columns

# <codecell>


