import pandas as pd
import os.path
from matcher import PdfSlider
from video import Video

class DataSet:
  def __init__(self, summary):
    self.summary = summary

  def summary_base_info(self):
    """ collect base information into summary
    """
    data = self.summary
    for pn in data[['n_name', 'n_root']].values:
      ps = PdfSlider(pn[0], pn[1])
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

  def summary_build_dir(self):
    """ Create folders needed for each dataset"""
    data = self.summary
    for pn in data[['n_name', 'n_root']].values:
      ps = PdfSlider(pn[0], pn[1])
      for si in ('thumb', 'mid', 'big'):
        fd = ps.slides_path(si)
        if not os.path.exists(fd):
          os.makedirs(fd)
          print pn
