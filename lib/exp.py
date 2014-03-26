# system
import os.path
import glob
# custom
from matcher import PdfSlider
from video import Video
# scientific
import cv2, cv
import numpy as np
import pandas as pd

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


class FeatsKp:
  def __init__(self, img):
    """
    """
    self.img = img

  def fast(self):
    """
    http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_fast/py_fast.html
    """

  def sift(self):
    """
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html
    """

  def surf(self):
    """
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html?highlight=surf
    """

  def brisk(self):
    """
    http://docs.opencv.org/trunk/modules/features2d/doc/feature_detection_and_description.html
    """

from multiprocessing import Process, Queue
from lib.handy import HandyStore as hs
class Prepare():
  def __init__(self, root, name):
    vid = glob.glob("./data/{}/{}/video.*".format(root, name))[0]
    self.vid = vid
    self.key = "./data/{}/{}/prepare".format( root, name)
    self.statq = self.cmdq = self.p = None

  def share_data(self, data):
    sq = self.statq
    if sq.full(): sq.get()
    sq.put_nowait(data)

  def get_cmd(self):
    cq = self.cmdq
    cmd = None
    if not cq.empty(): cmd = cq.get_nowait()
    return cmd

  def save_to(self, dkey, df):
    hdf = hs(self.key)
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

  def diff_base(self, key='base', end=-1, size=2):
    vid = Video(self.vid)
    fps = vid.cap['fps']
    ret = []
    for il in vid.scoped_frames(start=0, end=end, size=2, time_span=1000/fps):
      data = yield(il)
      ret.append( data )
      self.share_data( il[0]['ms']/(1000*end) )
      if self.get_cmd() == 'stop':
        print "Process terminated at frame {}".format(il[0]['fn'])
        break
    df = pd.DataFrame(ret, columns=['ms', 'frame_id', 'diff'])
    self.save_to("diff_{}_{}".format(key, end), df)

  def diff_next(self, end=-1):
    fdb = self.diff_base(key='next', end=end)
    il = fdb.next()
    while il:
      data = [ il[0]['ms'], il[0]['fn'],
        cv2.absdiff(il[0]['img'], il[-1]['img']).sum(),
        ]
      try:
        il = fdb.send( data )
      except StopIteration:
        break

  def diff_bkg(self, end=-1, sec=3):
    bgm = cv2.BackgroundSubtractorMOG(10, 6, 0.9, .1)
    fdb = self.diff_base(key='bkg', end=end)
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

  def cap_vital_frame(self, byfunc, end=-1):
    def func(*args, **kwargs): #unwrap function for local use
      return byfunc(*args, **kwargs)
    if not self.idle():
      print "{} is working for {}".format( self.key, self.p.name)
      return
    self.statq = Queue(3)
    self.cmdq = Queue(5)
    self.p = Process(target=func, kwargs={'end': end})
    self.p.start()


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
      ds.summary_extract_slides()
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

class GroundTruth:
  def __init__(self, gnd):
    """
    :gnd: the dataframe contained ground truth
    """
    self.gnd = gnd

  def aggregate(self):
    gf = self.gnd

