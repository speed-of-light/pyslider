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

class Summary:
  def __init__(self):
    self.sp = 'data/store.h5'
    self.load()

  def load(self, key='summary'):
    self.sdf = pd.read_hdf(self.sp, key, format='t')
    return self.sdf

  def save(self, key='summary', data=None):
    if data is None: data = self.df
    data.to_hdf(self.sp, key, mode='a', data_columns=True, format='t',
        complib='blosc', complevel=6)

  def info(self, root, name):
    df = self.sdf
    dr = df[df['n_root'].eq(root) & df['n_name'].eq(name)]
    return dr

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
