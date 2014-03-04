import cv2, cv
import collections, os
import numpy as np
import pandas as pd
import glob, os.path
class Matcher:
  """
  Author: speed-of-light
  Purpose: Operations on video frames
  """

  @property
  def data(self):
    """Using Pandas DataFrame
    """
    return self.df

  @property
  def db_root(self):
    """The root of slide images
    """
    return self.db_root

  @db_root.setter
  def db_root(self, value):
    """Set the image db root path
    value: string path
    """
    self.db_root = value
    self.load_img()

  def __init__(self, db_root=""):
    self.df = pd.DataFrame(columns=["img", 'sift'])
    self.db_root = db_root

  def __cs__(self, x, y):
    if int(x[7:]) > int(y[7:]): return 1
    elif int(x[7:]) == int(y[7:]): return 0
    else: return -1

  def load_img(self):
    """
    Load images with given db root
    """
    dr = self.db_root
    self.df = self.df[len(self.df):]
    igp = []
    for file in glob.glob("{}/*.jpg".format(dr)):
      igp.append(os.path.splitext( os.path.basename(file) )[0])
    igp.sort(cmp=self.__cs__)
    for imp in igp:
      self.df = self.df.append([dict(img=imp)], ignore_index=True)
    self.img_loaded = True

  def comp_feats(self, method='sift'):
    """Compute features with need
    """
    if not self.img_loaded: return False
    self.fdb = []
    for ip in self.data.img:
      im = "{}/{}.jpg".format(self.db_root, ip)
      im = cv2.imread(im, cv.CV_LOAD_IMAGE_GRAYSCALE)
      kp, des = self._sift(im)
      self.fdb.append( dict(keypoints=kp, desc=des, name=ip))

  def _good_matches(self, matches, threshold=.6):
    good = []
    for m,n in matches:
      if m.distance < n.distance * threshold:
        good.append(m)
    return good

  def _sift(self, gray=None):
    """Computes sift features
    """
    sift = cv2.SIFT()
    kp, des = sift.detectAndCompute( gray, None)
    return kp, des

  def _surf(self, gray):
    surf = cv2.SURF(4000)
    kp, des = surf.detectAndCompute( gray, None)
    return kp, des

  def _match_one(self, ia, ib):
    """Return good matches
    """
    FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing in python cv2
    flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 4)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(flann_params, search_params)
    matches = flann.knnMatch(ia, ib, k=2)
    return self._good_matches(matches)

  def _filter_homography(self, src_shape, ka, kb, mdes, method=cv2.RANSAC):
    """
    Get source image homography bound to destination
    Params:
      src_shape: width, height of input image
      ka: keypoints of image a
      kb: keypoints of image b
      mdes: good matches of a and b
      method:
        0 - a regular method using all the points
        CV_RANSAC - RANSAC-based robust method
        CV_LMEDS - Least-Median robust method
    Todos:
      Try dynamically set ransacReprojThreshold with dst's kp.size within 1 to 10.
    """
    good = mdes
    if len(good) >= self.MIN_MATCH_COUNT:
      src = np.float32( [ ka[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst = np.float32( [ kb[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src, dst, method=method, ransacReprojThreshold=5.0)
      #self.matchesMask = mask.ravel().tolist()
      h,w = src_shape
      pts = np.float32([ [0,0], [0,h-1], [w-1,h-1], [w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts, M)
      return np.int32(dst)
    else:
      print "Only {} matches are found (need {}).".format(len(good), self.MIN_MATCH_COUNT)
      return None

  def match(self, img):
    """Return matched result with image
    img: should be gray scale input
    """
    ikp, ikdes = self._sift(img)
    lst = []
    for feats in self.fdb:
      st = self._match_one(ikdes, feats['desc'])
      lst.append(len(st))
    return lst

  def plot(self, ptype):
    """TODO return key points plotted on given images
    """
    #img = cv2.drawKeypoints( img_src, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


from PyPDF2 import PdfFileReader
from pgmagick import Image
import shutil
class PdfSlider():
  """
  Author: speed-of-light
  Purpose: Operations on pdf files
  """
  @property
  def slide_path(self):
    """The root of slide images
    """
    return "./tmp/{}".format(self.filename)
  @property
  def pages(self):
    """The root of slide images
    """
    return self.pages

  def __init__(self, pdf_path):
    self.pdf_path = pdf_path
    pdf = PdfFileReader(self.pdf_path)
    self.pages = pdf.getNumPages()

  def to_jpg(self):
    pages = self.pages
    if pages < 1: return
    fn = self.filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
    tmpdf = "./tmp/{}".format(fn)
    if os.path.exists( tmpdf ): shutil.rmtree(tmpdf)
    os.makedirs( tmpdf )
    conv = Image()
    conv.density( '100')
    for page in np.arange( 0, pages, 1):
      conv.read( "{}[{}]".format(self.pdf_path, page) )
      conv.write( "{}/slides_{}.jpg".format(tmpdf, page) )
