# system
import os
import re
import shutil
import logging
import logging.handlers
# scientific
import pandas as pd
import cv2
# custom
from summary import Summary
from ..data import PdfReader
from ..emailer import Emailer


class ExpCommon(object):
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


class Slider(ExpCommon):
    """
    A class to handle slide data
    """
    def __init__(self, root="", name=""):
        self.root = root
        self.name = name

    def _blank_slide(self):
        sp = self.slides_path()
        img = cv2.imread("{}/{:03d}.jpg".format(sp, 1))
        img[:] = (255, 255, 255)  # fill white
        # red cross
        red = (0, 0, 255)
        line_width = int(0.1*img.shape[0])
        topL = (0, 0)
        botR = (img.shape[1], img.shape[0])
        topR = (0, img.shape[0])
        botL = (img.shape[1], 0)
        cv2.line(img, topL, botR, red, line_width)
        cv2.line(img, topR, botL, red, line_width)
        return img

    def _is_valid_sid(self, index, count):
        return (index > 0 and index < count+1)

    def _img_path(self, root, idx):
        return "{}/{:03d}.jpg".format(root, idx)

    def slide_pages(self):
        ps = Slider(self.root, self.name)
        return ps.pages()

    def slides_path(self, size='mid'):
        ps = PdfReader(self.root, self.name)
        return ps.slides_path(size)

    def get_slides(self, ids=[], gray=False, resize=None):
        """
        Get slide images collection
        """
        sp = self.slides_path(size='big')
        su = Summary()
        sin = su.info(self.root, self.name).iloc[0]
        if ids is None:
            ids = range(1, sin.n_slides+1)
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        for si in ids:
            sp = self._img_path(sp, si)
            if self._is_valid_sid(si, sin.n_slides):
                if gray:
                    img = cv2.imread(sp, cv2.COLOR_GRAY2BGR)
                else:
                    img = cv2.imread(sp)
            else:
                img = self._blank_slide()
                img = img[0] if gray else img
            if resize is not None:
                img = cv2.resize(img, resize)
            yield(dict(img=img, idx=si))

    def get_slide(self, index=1, resize=None):
        su = Summary()
        sin = su.info(self.root, self.name).iloc[0]
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        if self._is_valid_sid(index, sin.n_slides):
            spb = self.slides_path('big')
            img = cv2.imread(self._img_path(spb, index))
        else:
            img = self._blank_slide()
        if resize is not None:
            img = cv2.resize(img, resize)
        return img[:, :, [2, 1, 0]]  # convert for matplotlib
