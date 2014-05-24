import pandas as pd
from ..exp import ExpCommon
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
    gcf = self._aggregate(gf.copy())
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
