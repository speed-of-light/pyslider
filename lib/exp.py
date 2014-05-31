# system
import os
import re
import shutil
import logging
import logging.handlers
# scientific
import pandas as pd
# custom
from data import PdfSlider
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
    self.upass = None
    self._init_logger()

  def _init_logger(self):
    cn = self._underscore(self.__class__.__name__)
    fmt = logging. \
        Formatter(fmt='%(asctime)s,%(levelname)s,' +
                  '%(name)s,%(funcName)s,%(lineno)d, %(message)s',
                  datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger("{}.{}.{}.{}".
                               format(__name__, cn, self.root, self.name))
    logger.setLevel(logging.INFO)
    logger.propagate = 0
    # FileHandler
    fn = self.make_path('log', 'log', True, False)
    fnh = fn + "_fh"
    cnh = fn + "_ch"
    if fnh not in [lh.name for lh in logger.handlers]:
      fh = logging.handlers. \
          RotatingFileHandler(fn, maxBytes=10485760, backupCount=5)
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

  def make_path(self, resource='stores', ext='h5', asure=True, root=False):
    """
    resource: resource name in path
    ext: file extension for resource, if None then return only path
    asure: make sure the path exist
    root: get only root path of given resource
    usage:
      # make simple log path, and make sure created
      self.make_path('log', None)
      # make path for log with log extension, and not check existence
      self.make_path('log', 'log', False)
    """
    rt = self.root
    pn = self.name
    cn = self._underscore(self.__class__.__name__)
    pth = "data/{}/{}/{}".format(rt, pn, resource)
    if root:
      return pth
    if asure:
      self._asure_path(pth)
    pth = "{}/{}".format(pth, cn)
    if ext is not None:
      pth = "{}.{}".format(pth, ext)
    return pth

  def store_path(self):
    """
    DEPRECATED, use make_path instead.
    """
    return self.make_path()

  def delete_file(self, tar=[('store', 'h5', False)]):
    for res, ext, root in tar:
      ph = self.make_path(res, ext, False, root)
      print ph
      if ext is None or root:  # for whole directory
        shutil.rmtree(ph)
      else:  # for a single file
        if os.path.isfile(ph):
          os.remove(ph)

  def save(self, key, data):
    self.log.info('save key ==> {}'.format(key))
    sp = self.make_path('stores', 'h5', asure=True, root=False)
    data.to_hdf(sp, key, mode='a', data_columns=True, format='t',
                complib='blosc', complevel=self.comp)
    self._save_key(sp, key)

  def load(self, key):
    sp = self.store_path()
    try:
      df = pd.read_hdf(sp, key, format='t')
    except KeyError, e:
      print e
      return None
    return df

  def _save_key(self, fpath, key):
    kf = self.load('keys')
    if kf is None:
      kf = pd.DataFrame([key], columns=['key'])
    else:
      kf = kf.append(pd.DataFrame([key], columns=['key']))
      kf = kf.reset_index()
      for rc in ['index', 'level']:
        if rc in kf.columns:
          del kf[rc]
    kf.to_hdf(fpath, 'keys', mode='a', data_columns=True,
              format='t', complib='blosc', complevel=self.comp)

  def _underscore(self, string=''):
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
    ks = di.keys()
    ks.sort()
    for k in ks:
      s += "/{}_{}".format(k, di[k])
    return s

  def _asure_path(self, path):
    if not os.path.exists(path):
      os.makedirs(path)

  def notify(self, summary):
    if self.upass is None:
        return
    ps = self.upass
    cn = self._underscore(self.__class__.__name__)
    title = "Pyslider Job: {} <{}-{}> Finished". \
        format(cn, self.root, self.name)
    me = "speed.of.lightt@gmail.com"
    with Emailer(config=dict(uname=me, upass=ps)) as mailer:
      mailer.send(title, summary, ['speed.of.lightt@gmail.com'])


from _exp.prepare import Prepare
from _exp.feats import Feats
from _exp.matching import Matcher
from _exp.fetus import GroundTruth
from _exp.summary import Summary


class Prepare(Prepare):
    pass


class Feats(Feats):
    pass


class Matcher(Matcher):
    pass


class Summary(Summary):
    pass


class GroundTruth(GroundTruth):
    pass
