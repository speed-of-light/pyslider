import os
import cv2
import pandas as pd
import numpy as np
from ..exp import ExpCommon
from ..handy import HandyTimer as ht
from fetus import Summary

class Feats(ExpCommon):
  def __init__(self, root, name):
    """
    """
    ExpCommon.__init__(self, root, name)

  def __str__(self, mn=None):
    ret = "{}[{}]".format(self.root, self.name)
    if mn is not None: ret += " - {}".format(mn)
    return ret

  def o_frames(self, gray=False):
    pass

  def o_slides(self, gray=False, resize=None):
    """
    Get slide images collection
    """
    spm = self.slides_path(size='big')
    slides = [spm+"/"+name for name in os.listdir(spm) if os.path.isfile(spm+"/"+name)]
    for i, sp in enumerate(slides, 1):
      if gray: img = cv2.imread(sp, cv2.COLOR_GRAY2BGR)
      else: img = cv2.imread(sp)
      yield(dict(img=img, index=i))

  def comb_fm_list(self):
    """
    List combinations of each methods
    """
    kp_adp = ['', 'Grid', 'Pyramid']
    kp_algo = ["FAST", "FASTX","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"]
    kps = [dd[0]+dd[1] for dd in itertools.product(kp_adp, kp_algo)]
    des_adp = ['', 'Opponent']
    des_algo = ["SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"]
    des = [dd[0]+dd[1] for dd in itertools.product(des_adp, des_algo)]
    pkg = [dd for dd in itertools.product(kps, des)]
    return pkg

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
    self.log.info("param path => " + dkrk)
    for im in img_iter:
      imid = im['index']
      img = im['img']
      with ht(verbose=0) as ts:
        kps = fd.detect(img, None)
        kps, des = de.compute(img, kps)
      kdf = pd.DataFrame([[ kp.pt[0], kp.pt[1], kp.size, kp.angle,
        kp.response, kp.octave, kp.class_id] for kp in kps], columns = cols)
      ddf = pd.DataFrame(des)
      kdf[kdf.columns] = kdf[kdf.columns].astype(kdf['x'].dtype)
      ddf.columns = [("i_" + str(cc)) for cc in ddf.columns]
      self.save("{}/i{:03d}".format(dkrk, imid), kdf)
      self.save("{}/i{:03d}".format(dkrd, imid), ddf)
      llog = pd.DataFrame([[int(ts.msecs), len(des)]], columns=['ms', 'kps'] )
      dlog = dlog.append( llog)
      self.log.info(self.__str__("sid[{}] ".format(imid)) + str(ts.msecs) )
    dklg = self._df_key_root(mod, opts, img_type, dtype='log')
    dlog = dlog.reset_index()
    del dlog['index']
    dlog[dlog.columns] = dlog[dlog.columns].astype(np.uint32)
    self.save(dklg, dlog)
    self.log.info("fn finished" + dkrk)
    return dlog

  def run_all_slides(self, np=''):
    cfl = self.comb_fm_list()
    with ht() as ts:
      for cc in cfl:
        osl = self.o_slides(gray=('Opponent' not in cc[1]))
        try:
          self.detect_with(img_iter=osl, img_type='slide',
            mod=dict( kp_algo=cc[0], des_algo=cc[1]))
        except Exception as e:
          self.log.error("<<{}-{}>>: {}".format(cc[0], cc[1], e))
          continue
    self.notify("Time: {}".format(ts.tstr()))

  def _df_key_root(self, mod, opt, set_name='slide', dtype='kp'):
    hdfk = "/{}/{}".format(mod['kp_algo'], mod['des_algo'])
    us = self._ustr_dict(opt)
    fik = "{}{}/{}/{}".format(hdfk, us, set_name, dtype)
    return fik

  def _set_extractor(self, exc, opts={}):
    def set_value(exc, name, value):
      dtype = exc.paramType(name)
      if dtype == 0 or dtype==10: exc.setInt(name, int(value))
      elif dtype == 1: exc.setBool(name, bool(value))
      elif dtype == 2: exc.setDouble(name, double(value))
      elif dtype == 3: exc.setString(name, str(value))
    for dk in opts.keys():
      set_value(exc, dk, opts[dk])
    if 0:
      for p in de.getParams():
        res = get_value(de, p)
        print p, res

  def _get_exc_value(self, exc, name):
    dtype = exc.paramType(name)
    if dtype == 0 or dtype==10: v = exc.getInt(name)
    elif dtype == 1: v = exc.getBool(name)
    elif dtype == 2: v = exc.getDouble(name)
    elif dtype == 3: v = exc.getString(name)
    va = ['Int', 'Bool', 'Double', 'Str', '-', '-', '-', '-', '-', '-', 'Short']
    return (va[dtype], v)

  def detect_match_with(self, fr_list=[],
      mod=dict(kp_algo='FAST', des_algo='SIFT')):
    """
    Detect and find best matched result from slides results
    """
    fd = cv2.FeatureDetector_create(mod['kp_algo'])
    de = cv2.DescriptorExtractor_create(mod['des_algo'])
    for im in img_iter:
      iid = im['index']; img = im['img']
      with ht(verbose=0) as ts:
        kps = fd.detect(img, None)
        kps, des = de.compute(img, kps)

  def _unpickle_keypoints(self, kdf):
    if kdf is None: return None
    kps = []
    for ki in kdf.index:
      kd = kdf.ix[ki]
      ktmp = cv2.KeyPoint(x=kd['x'], y=kd['y'],
          _size=kd['size'], _angle=kd['angle'],
          _response=kd['response'], _octave=int(kd['octave']),
          _class_id=int(kd['class_id']))
      kps.append(ktmp)
    return kps

  def resrc(self):
    """
    http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_fast/py_fast.html
    sift http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html
    surf http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html?highlight=surf
    brisk http://docs.opencv.org/trunk/modules/features2d/doc/feature_detection_and_description.html
    """
    pass

  def load_feats(self,
      mod=dict(kp_algo='FAST', des_algo='SIFT')):
    su = Summary()
    n_slid = su.info(self.root, self.name)['n_slides']
    key_root = "/{kp_algo}/{des_algo}/slide".format(**mod)
    sfd = []
    for ns in range(1, n_slid+1):
      kk = key_root + "/kp/i{:03d}".format(ns)
      dk = key_root + "/desc/i{:03d}".format(ns)
      kps = self._unpickle_keypoints( self.load(kk) )
      des = self.load(dk)
      des = None if des is None else des.values
      sfd.append(dict(idx=ns, kps=kps, des=des))
    return sfd

  def single_feats(self, img,
      mod=dict(kp_algo='FAST', des_algo='SIFT')):
    fd = cv2.FeatureDetector_create(mod['kp_algo'])
    de = cv2.DescriptorExtractor_create(mod['des_algo'])
    ks = fd.detect(img)
    ks, ds = de.compute(img, ks)
    return ks, ds


class Matcher(ExpCommon):
  def __init__(self, root, name):
    """
    Get effective frame lists from prepared data
    """
    ExpCommon.__init__(self, root, name)

  def single_match(self, dquery, dtrain, mtype="BruteForce", thres=.5):
    """
    BruteForce-L1 BruteForce-Hamming BruteForce-Hamming(2) FlannBased
    """
    mat = cv2.DescriptorMatcher_create(mtype)
    #mre = mat.match(dquery, dtrain)
    mra = mat.knnMatch(dquery, dtrain, k=2)
    mre = []
    for m,n in mra:
      if m.distance < n.distance*thres:
        mre.append(m)
    mra = []
    for re in mre:
      mra.append([re.queryIdx, re.trainIdx, re.imgIdx, re.distance])
    if len(mra) is 0:
      return pd.DataFrame(columns=['qix', 'tix', 'iix', 'dt'])
    else:
      return pd.DataFrame(mra, columns=['qix', 'tix', 'iix', 'dt'])

  #binary
  def tmp(self):
    """
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_brief/py_brief.html?highlight=brief
    http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_orb/py_orb.html?highlight=orb
    http://stackoverflow.com/questions/20146570/opencv-python-dense-sift
    http://stackoverflow.com/questions/14588682/freak-descriptor-with-opencv-python
    def color_hist(self):
    def text_region(self):
    http://answers.opencv.org/question/19015/how-to-use-mser-in-python/
    https://opencv-code.com/tutorials/automatic-perspective-correction-for-quadrilateral-objects/
    """

  def plot_match(self, qimg, qkp, timg, tkp, match):
    h1, w1 = qimg.shape[:2]; h2, w2 = timg.shape[:2]
    view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    view[:h1, :w1] = qimg; view[:h2, w1:] = timg
    for mi in match.index:
      tix = int(match.ix[mi]['tix']); qix = int(match.ix[mi]['qix'])
      color = tuple([np.random.randint(0, 255) for _ in xrange(3)])
      qmp = (int(qkp[qix].pt[0]), int(qkp[qix].pt[1]))
      tmp = (int(tkp[tix].pt[0] + w1), int(tkp[tix].pt[1]))
      cv2.line(view, qmp, tmp, color)
    return view
