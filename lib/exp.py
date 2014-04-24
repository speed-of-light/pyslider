# system
import os, glob, re, itertools, logging
from multiprocessing import Process, Queue, Lock
from memory_profiler import memory_usage as mu
# scientific
import cv2, cv
import numpy as np
import pandas as pd
# plotting
from matplotlib import offsetbox as ofb
# custom
from matcher import PdfSlider
from video import Video
from handy import HandyStore as hs
from handy import HandyTimer as ht
from emailer import Emailer

class ExpCommon():
  def __init__(self, root, name):
    """
    `root`: file root
    `name`: project name
    """
    self.root = root
    self.name = name
    self.comp = 6
    self._init_logger()

  def _init_logger(self):
    cn = self._underscore(self.__class__.__name__)
    fmt = logging.Formatter(fmt= '%(asctime)s,%(levelname)s,'+
        '%(name)s,%(funcName)s,%(lineno)d, %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger("{}.{}".format(__name__, cn))
    logger.setLevel(logging.INFO)
    logger.propagate = 0
    # FileHandler
    fp = "log/{}_{}".format(self.root, self.name)
    self._asure_path(fp)
    fn = "{}/{}.log".format(fp, cn)
    fnh = fn + "_fh"; cnh = fn + "_ch"
    if fnh not in [lh.name for lh in logger.handlers]:
      fh = logging.handlers.RotatingFileHandler(fn, maxBytes=10485760, backupCount=5)
      fh.name = fnh
      fh.setFormatter(fmt)
      logger.addHandler(fh)
    # StreamHandler
    if 0 and cnh not in [lh.name for lh in logger.handlers]:
      ch = logging.StreamHandler()
      ch.name = cnh
      ch.setFormatter(fmt)
      logger.addHandler(ch)
    logger.info(">>============== {} inited ================= <<".format(cn))
    self.log = logger

  def slide_pages(self):
    ps = PdfSlider(self.name, self.root)
    return ps.pages()

  def slides_path(self, size='mid'):
    ps = PdfSlider(self.name, self.root)
    return ps.slides_path(size)

  def store(self):
    sp = self.store_path()
    return pd.HDFStore(sp, format='t', data_columns=True,
        complib='blosc', complevel=self.comp)

  def store_path(self):
    rt = self.root
    pn = self.name
    cn = self._underscore(self.__class__.__name__)
    return "data/{}/{}/stores/{}.h5".format( rt, pn, cn)

  def delete_file(self):
    if os.path.isfile(self.store_path()): os.remove(self.store_path())

  def save(self, key, data):
    sp = self.store_path()
    data.to_hdf(sp, key, mode='a', data_columns=True,
         format='t', complib='blosc', complevel=self.comp)
    kf = self.load('keys')
    if kf is None: kf = pd.DataFrame([key], columns=['key'])
    else:
      kf = kf.append(pd.DataFrame([key], columns=['key']))
      kf = kf.reset_index()
      for rc in ['index', 'level']:
        if rc in kf.columns: del kf[rc]
    kf.to_hdf(sp, 'keys', mode='a', data_columns=True,
        format='t', complib='blosc', complevel=self.comp)

  def load(self, key):
    sp = self.store_path()
    try:
      df = pd.read_hdf(sp, key, format='t')
    except KeyError, e:
      return None
    return df

  def _underscore(self, string):
    # move pre-compile out the loop to improve performance
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1_\2', string)
    return all_cap_re.sub(r'\1_\2', s1).lower()

  def _ustr_dict(self, di):
    """
    Make dict keys underscore for saving to hdfs
    """
    s = ""
    ks = di.keys(); ks.sort()
    for k in ks: s += "/{}_{}".format( k, di[k])
    return s

  def _asure_path(self, path):
    if not os.path.exists(path): os.makedirs(path)


#class ExpScheduler():


class Refine:
  # time series relation ship
  def hmm(self):
    ""

  def mdp(self): #markov_decision_process
    ""

  def gaussian_scope_modeling(self):
    ""

  def time_scope(self):
    ""

  def dtw(self):
    """
    https://gist.github.com/socrateslee/3265694
    """

# find slide region
  def ransac(self):
    ""

  def hough_rect(self):
    ""


class Matching:
  def compare_hist(self):
    """
    http://docs.opencv.org/doc/tutorials/imgproc/histograms/histogram_comparison/histogram_comparison.html
    """

  def svm(self):
    """
    """

  def pca(self):
    ""

  def brute_force(self):
    ""

  def flann(self):
    ''


class FeatsDesc:
  def __init__(self, img):
    """
    """
    self.img = img

  #binary
  def brief(self):
    """
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_brief/py_brief.html?highlight=brief
    """

  def orb(self):
    """
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html?highlight=orb
    """

  # scale
  def sift(self):
    """
    http://stackoverflow.com/questions/20146570/opencv-python-dense-sift
    """
    ""

  def surf(self):
    ""

  def freak(self):
    """
    http://stackoverflow.com/questions/14588682/freak-descriptor-with-opencv-python
    """
    ""

  # others
  def color_hist(self):
    """
    """

  def text_region(self):
    """
    """

  def mser(self):
    """
    http://answers.opencv.org/question/19015/how-to-use-mser-in-python/
    """

  #matchers
  def bruteforce(self):
    """
    """

  def flann(self):
    """
    """

  def ransac(self):
    """
    https://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/
    """


class Feats(ExpCommon):
  def __init__(self, root, name):
    """
    """
    ExpCommon.__init__(self, root, name)

  def o_slides(self, gray=False):
    spm = self.slides_path(size='big')
    slides = [spm+"/"+name for name in os.listdir(spm) if os.path.isfile(spm+"/"+name)]
    for i, sp in enumerate(slides, 1):
      if gray: img = cv2.imread(sp, cv2.COLOR_GRAY2BGR)
      else: img = cv2.imread(sp)
      yield(dict(img=img, index=i))

  def detect_with(self, img_iter=[], img_type='slide',
      mod=dict( kp_algo='FAST', des_algo='SIFT'), **opts):
    """
    `mod` dict should include
      `kp_adp`: '', 'Grid', 'Pyramid' #adaptive method for detection
      `kp_algo`: "FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"
      `des_adp`: '', 'Opponent'
      `des_algo`: "SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"
    """
    fd = cv2.FeatureDetector_create(mod['kp_algo'])
    de = cv2.DescriptorExtractor_create(mod['des_algo'])
    #if det.empty(): return None
    cols = [ 'x', 'y', 'size', 'angle', 'response', 'octave', 'class_id']
    dkrk = self._df_key_root(mod, opts, img_type)
    dkrd = self._df_key_root(mod, opts, img_type, dtype='desc')
    dlog = pd.DataFrame(columns=['ms', 'kps']).convert_objects()
    self.log.info("param path" + dkrk)
    for im in img_iter:
      imid = im['index']
      img = im['img']
      with ht(verbose=0) as ts:
        kps = fd.detect(img, None)
        kps, des = de.compute(img, kps)
      dlog = dlog.append( pd.DataFrame([[int(ts.msecs), len(des)]], columns=['ms', 'kps']))
      kdf = pd.DataFrame([[ kp.pt[0], kp.pt[1], kp.size, kp.angle,
        kp.response, kp.octave, kp.class_id] for kp in kps], columns = cols)
      ddf = pd.DataFrame(des)
      kdf[kdf.columns] = kdf[kdf.columns].astype(kdf['x'].dtype)
      ddf.columns = [("i_" + str(cc)) for cc in ddf.columns]
      self.save("{}/i{:03d}".format(dkrk, imid), kdf)
      self.save("{}/i{:03d}".format(dkrd, imid), ddf)
      self.log.info(self.__str__("sid[{}] ".format(imid)) + str(ts.msecs) )
    dklg = self._df_key_root(mod, opts, img_type, dtype='log')
    dlog = dlog.reset_index()
    del dlog['index']
    dlog[dlog.columns] = dlog[dlog.columns].astype(np.uint32)
    self.save(dklg, dlog)
    self.log.info("fn finished" + dkrk)
    return dlog

  def __str__(self, mn=None):
    ret = "{}[{}]".format(self.root, self.name)
    if mn is not None: ret += " - {}".format(mn)
    return ret

  def _df_key_root(self, mod, opt, set_name='slide', dtype='kp'):
    hdfk = "/{}/{}".format(mod['kp_algo'], mod['des_algo'])
    us = self._ustr_dict(opt)
    fik = "{}{}/{}/{}".format(hdfk, us, set_name, dtype)
    return fik

  def comb_fm_list(self):
    """
    List combinations of each methods
    """
    kp_adp = ['', 'Grid', 'Pyramid']
    kp_algo = ["FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"]
    kps = [dd[0]+dd[1] for dd in itertools.product(kp_adp, kp_algo)]
    des_adp = ['', 'Opponent']
    des_algo = ["SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"]
    des = [dd[0]+dd[1] for dd in itertools.product(des_adp, des_algo)]
    pkg = [dd for dd in itertools.product(kps, des)]
    return pkg

  def set_extractor(self, exc, opts={}):
    def set_value(exc, name, value):
      dtype = exc.paramType(name)
      if dtype == 0 or dtype==10: exc.setInt(name, int(value))
      elif dtype == 1: exc.setBool(name, bool(value))
      elif dtype == 2: exc.setDouble(name, double(value))
      elif dtype == 3: exc.setString(name, str(value))
    for dk in opts.keys():
      set_value(exc, dk, opts[dk])
    #for p in de.getParams():
    #  res = get_value(de, p)
    #  print p, res

  def get_exc_value(self, exc, name):
    dtype = exc.paramType(name)
    if dtype == 0 or dtype==10: v = exc.getInt(name)
    elif dtype == 1: v = exc.getBool(name)
    elif dtype == 2: v = exc.getDouble(name)
    elif dtype == 3: v = exc.getString(name)
    va = ['Int', 'Bool', 'Double', 'Str', '-', '-', '-', '-', '-', '-', 'Short']
    return (va[dtype], v)

  def run_all_slides(self, np=''):
    cfl = self.comb_fm_list()
    osl = self.o_slides(gray=True)
    self.log.info('here')
    with ht() as ts:
      for cc in cfl:
        self.detect_with(img_iter=osl, img_type='slide',
          mod=dict( kp_algo=cc[0], des_algo=cc[1]))
    with Emailer(config=dict(uname="speed.of.lightt@gmail.com", upass=np)) as mailer:
      mailer.send("Feats Job [{}][{}] Finished".format(self.root, self.name),
        "Time: {}".format(ts.tstr()), 'speed.of.lightt@gmail.com')

  def tmp(self):
    """
    http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_fast/py_fast.html
    sift http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html
    surf http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html?highlight=surf
    brisk http://docs.opencv.org/trunk/modules/features2d/doc/feature_detection_and_description.html
    """


class Prepare():
  def __init__(self, root, name):
    self.root = root
    self.pj_name = name
    self.statq = self.cmdq = self.p = None

  def path(self):
    rt = self.root
    pn = self.pj_name
    return "./data/{}/{}/stores/prepare".format( rt, pn)

  def share_data(self, data):
    sq = self.statq
    if sq is None: return
    if sq.full(): sq.get()
    sq.put_nowait(data)

  def get_cmd(self):
    cq = self.cmdq
    if cq is None: return
    cmd = None
    if not cq.empty(): cmd = cq.get_nowait()
    return cmd

  def save_to(self, dkey, df):
    hdf = hs(self.path)
    ks = hdf.store.keys()
    if dkey in ks: hdf.store.remove(dkey)
    hdf.put(dkey, df)
    hdf.store.close()

  def diff(self, key='base', end=-1, size=2):
    vid = Video(self.vid)
    fps = vid.cap['fps']
    ret = []
    bgm = cv2.BackgroundSubtractorMOG(10, 6, 0.9, .1)
    for il in vid.scoped_frames(start=0, end=end, size=2, time_span=1000/fps):
      fgmask = bgm.apply(il[0]['img'])
      data = [ il[0]['ms'], il[0]['fn'], fgmask.sum() ]
      ret.append( data )
    return ret

  def diff_base(self, lock, key='base', end=-1, size=2):
    vid = Video(self.vid)
    fps = vid.cap['fps']
    end = vid.cap['seconds'] if (end == -1 or end > vid.cap['seconds']) else end
    ret = []
    for il in vid.scoped_frames(start=0, end=end, size=size, time_span=1000/fps):
      data = yield(il)
      ret.append( data )
      self.share_data(dict(prog=il[0]['ms']/(1000*end)))
      if self.get_cmd() == 'stop':
        print "Process terminated at frame {}".format(il[0]['fn'])
        break
    df = pd.DataFrame(ret, columns=['ms', 'frame_id', 'diff'])
    self.share_data(dict(prog=1.0))
    if lock is not None:
      lock.acquire(timeout=180)
      self.save_to("diff_{}".format(key), df)
      lock.release()

  def diff_next(self, lock, end=-1, size=2):
    dk = "next/size_{}".format(size)
    fdb = self.diff_base(lock, key=dk, end=end, size=size)
    il = fdb.next()
    while il:
      ratio = 1.0/len(il)
      mix = il[0]['img']
      mix = cv2.addWeighted(mix, ratio, mix, 0, 0)
      for i, img in enumerate(il):
        if i == 0 : continue
        mix = cv2.addWeighted(mix, 1, img['img'], ratio, 0)
      suma = cv2.absdiff(il[-1]['img'], mix).sum()
      data = [ il[0]['ms'], il[0]['fn'], suma ]
      try:
        il = fdb.send( data )
      except StopIteration:
        break

  def diff_bkg(self, lock, end=-1, hist=30, bgr=0.9, nog=5, nr=.1):
    bgm = cv2.BackgroundSubtractorMOG(hist, nog, bgr, nr)
    # TODO: dfk does not support keys like 3.x test.name etc..
    dfk = "bkg/hist_{}/bgr_{}/nog_{}/nr_{}".format(hist, bgr, nog, nr)
    fdb = self.diff_base(lock, key=dfk, end=end)
    il = fdb.next()
    while il:
      fgmask = bgm.apply(il[0]['img'])
      data = [ il[0]['ms'], il[0]['fn'], fgmask.sum() ]
      try:
        il = fdb.send( data )
      except StopIteration:
        break

  def stop(self):
    if self.idle(): return
    self.cmdq.put_nowait("stop")
    proc = self.p
    while not self.statq.empty():
      time.sleep(2)
      self.statq.get_nowait()
    if proc and proc.is_alive():
      proc.join()
      proc.terminate()

  def idle(self):
    balive = self.p and self.p.is_alive()
    sqnpt = self.statq and self.statq.empty()
    cqnpt = self.cmdq and self.cmdq.empty()
    return not ( balive and sqnpt and cqnpt )

  def cap_vital_frame(self, byfunc, **kwargs):
    def func(*args, **kwa): #unwrap function for local use
      for kw in kwa['kw_list']:
        fn = kw['fn']
        parl = kw['params']
        for par in parl:
          with ht(verbose=True) as t:
            #byfunc(*args, **kw)
            mus = mu((fn, args, par), interval=.0, timeout=None, max_usage=False)
          self.finq.put_nowait(dict(keys=par, name=fn.__name__,
            mem=mus[0], time=t.msecs))
      self.current_job = None
    if not self.idle():
      print "{} is working for {}".format( self.path, self.p.name)
      return
    lock = Lock()
    self.statq = Queue(3)
    self.cmdq = Queue(5)
    self.finq = Queue(500)
    self.p = Process(target=func, args=(lock,), kwargs=kwargs)
    self.p.start()

  def seq_reduce(self, df, value_key='diff'):
    """
    Keep max value in each continued sequence.
    ex:
     index = [ 1, 2, 3, 4, 7, 8, 9, 12, 13]
     value = [ 4, 2, 3, 3, 5, 8, 7,  8,  9]
     =>
     index = [ 1, 8, 13]
     value = [ 4, 8,  9]
    """
    igmax = -1; last_v = -1
    for i, v in enumerate(df.index):
      if i == 0:
        igmax = v
        next
      if (v - last_v) == 1: # check conti series max
        if df.ix[igmax][value_key] < df.ix[v][value_key]:
          df = df.drop([igmax])
          igmax = v
        else:
          df = df.drop([v])
      else:
        igmax = v
      last_v = v
    return df

  def plot_annote(self, ax, raw, gnd, nodes, ffrom=0, fto=2000):
    """
    `ax`: axes for plot area
    `raw`: raw data for observation
    `gnd`: ground truth data
    `nodes`: nodes dict contained
      (index array, value array, text array) for marking
      important data.
    `section`: data range to display
    `window_size`: data size to display
    """
    def add_artist(ax, fid, pval, bounce=(.5,.5), img=None):
      if img is None: img = vid.get_frame(by='id', value=fid)
      oft = ofb.OffsetImage(img, zoom=0.1)
      ab = ofb.AnnotationBbox(oft, (fid, pval), xycoords='data', xybox=bounce,
        boxcoords=('axes fraction', "axes fraction"), bboxprops=dict(boxstyle='round,pad=0.1', ec='g'),
        arrowprops=dict(arrowstyle="->", color='g'))
      ax.add_artist(ab)
    vid = Video(self.root, self.pj_name)
    slid = PdfSlider(self.pj_name, self.root)
    xlim = (ffrom, fto)
    # plot diff value
    ln_raw = ax.plot(raw, color='black')
    ln_peak = ax.plot([ii['index'] for ii in nodes], [vv['value'] for vv in nodes], 'ro')
    # plot ground truth
    ax2 = ax.twinx()
    ln_gnd = ax2.plot(gnd['fid'], gnd['sid'], 'b-')
    rng_sid = gnd[(gnd['fid'] > ffrom) & (gnd['fid'] < fto)].sid
    ax2.set_ylim( rng_sid.min()-1, rng_sid.max() + 1)
    ax.set_xlim(xlim)
    # make legend
    lns = ln_raw + ln_peak + ln_gnd
    labs = [l.get_label() for l in lns]
    ax.legend(lns, ['raw', 'peak', 'ground'], loc=0)
    for nod in nodes:
      inx = nod['index']; nov = nod['value']; gsid = int(nod['gsid'])
      if inx < xlim[0]: continue
      if inx > xlim[1]: break
      frac = (inx-ffrom)*1.0/(fto-ffrom)
      add_artist(ax, inx - 1, nov, (frac-0.05, .65))
      # last
      add_artist(ax, inx, nov, (frac, .95))
      add_artist(ax, inx, nov, (frac, .05), img=slid.get_slide(gsid))
      oft = ofb.TextArea("{}[{}]".format(inx, gsid))
      ab = ofb.AnnotationBbox(oft, (inx, nov), xycoords='data',
        xybox=(inx, 0.90), boxcoords=('data', "axes fraction"), bboxprops=dict(boxstyle='round,pad=0.1', ec='g'),
        arrowprops=dict(arrowstyle="->", color='g'))
      ax.add_artist(ab)
      # last
      add_artist(ax, inx + 1, nov, (frac+0.05, .8))


class Summary:
  def __init__(self, summary):
    """
    :summary: dataframe must have 'n_name' and 'n_root'
    :set:
    """
    self.summary = summary

  def talk_info_list(self):
    data = self.summary
    for pn in data[['n_name', 'n_root']].values:
      yield pn

  def ps_list(self):
    data = self.summary
    for pn in data[['n_name', 'n_root']].values:
      ps = PdfSlider(pn[0], pn[1])
      yield ps

  def base_info(self):
    """ collect base information into summary
    """
    data = self.summary
    for ps in self.ps_list():
      vs = Video(glob.glob("./data/{}/{}/video.*".format(pn[1], pn[0]))[0])
      vsc = vs.cap
      rv = data[data.n_name == pn[0]].index.values
      data['n_time'][rv] = int(vsc['seconds'])
      data['n_frames'][rv] = int(vsc['frames'])
      if ps.pages is None:
        data['n_slides'][rv] = len(glob.glob1("./data/{}/{}/slides".format(pn[1],
          pn[0]),"*.jpg"))
        continue
      data['n_slides'][rv] = ps.pages
    # change type for hdf saving
    scol = ['n_frames', 'n_slides', 'n_time']
    data[scol] = data[scol].astype(np.int)

  def extract_slides(self):
    """ Create folders needed for each dataset
    :example:
      from lib.exp import DataSet
      ds = DataSet(data)
      ds.extract_slides()
    """
    for ps in self.ps_list():
      for si in ('thumb', 'mid', 'big'):
        if ps.pages is None: continue
        ps.to_jpgs(size=si)
        print ps.pdf_path

  def mark_table(self, key, columns, values):
    """ Mark generated data for specific talk
    :key: data key
    :values: array that contained with (talk, existed) pair
    """
    sda = self.summary
    cols = sda.columns if columns is None else columns
    data = sda[sda.n_name.isin([ c for c in cols])]
    print len(data)
    for v in data[['n_name', 'n_root']].values:
      print v

class GroundTruth(ExpCommon):
  def __init__(self, root, name):
    ExpCommon.__init__(self, root, name)

  def univ_df(self):
    coll = []
    gnd = "data/{}/{}/ground_truth".format(self.root, self.name)
    with open(gnd, 'r') as f:
      for ln in f.readlines():
        cols = [int(x) for x in ln.split(',')]
        coll.append(cols)
    gf = pd.DataFrame(data=coll, columns=['fid', 'sid', 'slide_type', 'cam_status'])
    gcf = self._aggregate(gf.clone())
    return gcf

  def _aggregate(self, df):
    f_slid = -1; f_cnt = 1; f_keep=-1
    for inx in df.index:
      if f_slid < 0: f_slid = df.ix[inx]['sid']; continue
      if f_slid == df.ix[inx]['sid']:
        if f_cnt == 1: f_cnt = 2; f_keep = inx; continue
        if f_cnt > 1: df = df.drop(f_keep)
        f_keep = inx
      else:
        f_cnt = 1
        f_slid = df.ix[inx]['sid']
        continue
    return df

  def frame_gnd_tag(res, gnd):
    candi = []
    for di in res.index:
      qry = gnd[(gnd['fid'] <= di)]
      if len(qry) > 0: candi.append(qry.values[-1][1])
      else: candi.append(-1)
    res['ground_sid'] = candi


