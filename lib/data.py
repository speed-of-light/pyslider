import cv2, cv
import collections, os, os.path
import numpy as np
import pandas as pd
import glob

class Video:
  """
  Author: speed-of-light
  Purpose: Operations on video frames
  """

  @property
  def stream_path(self):
    return self.stream_path

  @stream_path.setter
  def stream_path(self, value):
    self.stream_path = value

  @property
  def cap(self):
    if self.stream_path == "":
      return ""
    else:
      cap = cv2.VideoCapture(self.stream_path)
      fps = cap.get(cv.CV_CAP_PROP_FPS)
      frs = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
      ret = {
        "cap": cap,
        "fps": fps,
        "frames": frs,
        "seconds": frs/fps
      }
      return ret

  @classmethod
  def from_path(self, stream_path=""):
    self.stream_path = stream_path

  def __init__(self, root, name):
    vid = glob.glob("./data/{}/{}/video.*".format(root, name))[0]
    self.stream_path = vid

  def scoped_frames(self, start=0, end=-1, size=1, time_span=1000):
    """
    Return a generator to manipulate with frames

    Parameters
    ----------
    start: millisecond
    end: millisecond, -1 to auto detect
    size: scoped size to dump frames
    time_span: 1000ms

    Returns
    -------
    Image and it's timestamp in milliseconds
    """

    if self.cap == "": yield None, None
    capr = self.cap
    cap = capr['cap']
    i = 0 if start < 0 else start
    fin = capr['seconds'] if (end == -1 or end > capr['seconds']) else end
    fin = fin* 1000 #time range in ms
    iset = collections.deque([])
    while True:
      k = i*time_span
      if k > fin: break
      cap.set(cv.CV_CAP_PROP_POS_MSEC, k)
      grabed, img = cap.read()
      if grabed:
        iset.append( dict(img=img,
          fn=cap.get(cv.CV_CAP_PROP_POS_FRAMES),
          ms=cap.get(cv.CV_CAP_PROP_POS_MSEC)) )
        if len(iset) > size: iset.popleft()
        yield(iset)
      i += 1

  def get_frames(self, ids=[], gray=False):
    cap = self.cap['cap']
    for fid in ids:
      cap.set(cv.CV_CAP_PROP_POS_FRAMES, fid)
      grabed, img = cap.read()
      if grabed:
        if gray: img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        yield(dict(img=img, idx=fid))

  def get_frame(self, by='id', value=0):
    key = dict(time=cv.CV_CAP_PROP_POS_MSEC, id=cv.CV_CAP_PROP_POS_FRAMES)
    cap = self.cap['cap']
    cap.set(key[by], value)
    grabed, img = cap.read()
    return img[:,:,[2,1,0]]  #convert for matplotlib

  def diff_pre(self, start=0, end=-1, fence="mild"):
    """
    Make absdiff of 2 images, return an array of the value and timestamp in ms.

    Params
    ------
    fence: statistical term to describe outlier range, "mild" and "extreme", use
      number for custom value.
    """
    data = np.array( [[0,0]] )
    for imgs in self.scoped_frames(start=start, end=end, size=2):
      iis = [img['img'] for img in imgs]
      cur = len(imgs) - 1
      pre = cur - 1
      dst = cv2.absdiff(iis[cur], iis[pre])
      data = np.append( data, [[ dst.sum(), imgs[cur]['ms'] ]], 0)
    df = pd.DataFrame(data[1:], columns=['isum','ms'])
    iqt = dict(mild=1.5, extreme=3, custom=fence)
    fence = "custom" if type(fence) is int else fence
    iqr = (df.isum.quantile(.75) - df.isum.quantile(.5))*iqt[fence]
    return df[df.isum.gt(iqr)]


from lib._exp.summary import Summary
from PyPDF2 import PdfFileReader
import shutil
#from wand.image import Image, Color
from pgmagick import Image
from PIL import Image as pimg
class PdfSlider():
  """
  Author: speed-of-light
  Purpose: Operations on pdf files
  """
  def slides_path(self, size="mid"):
    """The root of converted slide images
    """
    rt = self.root if self.root == "" else "{}/".format(self.root)
    return "./data/{1}{0}/slides/{2}".format(self.name, rt, size)

  @property
  def pdf_path(self):
    """The root of converted slide images
    """
    rt = self.root if self.root == "" else "{}/".format(self.root)
    return "./data/{1}{0}/{0}.pdf".format(self.name, rt)

  @property
  def pages(self):
    """The root of slide images
    """
    return self.pages

  def __init__(self, name="", root=""):
    """ Init data with project name and root dir
      root: base dir of pdf and video data
    """
    self.root = root
    self.name = name
    self.pages = None
    if os.path.isfile(self.pdf_path):
      pdf = PdfFileReader(self.pdf_path)
      self.pages = pdf.getNumPages()

  def png_jpg(self, path):
    png = "{}.png".format(path)
    jpg = "{}.jpg".format(path)
    pimg.open(png).convert('RGB').save(jpg)
    os.remove(png)

  def to_jpgs(self, size='mid', pages=None):
    """ Convert pdf to jpeg images
      pages: array for pages, None for extract all
    """
    dendic = dict( thumb=40, mid=100, big=150)
    density = dendic[size]
    pages = np.arange( 0, self.pages, 1) if pages is None else pages
    if len(pages) < 1: return
    sp = self.slides_path(size)
    if os.path.exists(sp): shutil.rmtree(sp)
    os.makedirs(sp)
    img = Image()
    img.density("{}".format(density))
    for page in pages:
      if page > self.pages or page < 0: continue
      pdf = "{}[{}]".format(self.pdf_path, page)
      slid = "{}/{:03d}".format(sp, page)
      img.read(pdf)
      img.write("{}.jpg".format(slid))
    #break
    #self.png_jpg('test.png')

  def get_slide(self, index=1, resize=None):
    su = Summary(); sin = su.info(self.root, self.name).iloc[0]
    if resize == True: resize=(sin.v_width, sin.v_height)
    if index < 1:
      img = cv2.imread( "{}/{:03d}.jpg".format(self.slides_path(), 1) )
      img[:] = (255,255,255)
      cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0,0,255), int(0.1*img.shape[0]))
      cv2.line(img, (0, img.shape[0]), (img.shape[1], 0), (0,0,255), int(0.1*img.shape[0]))
    else:
      img = cv2.imread( "{}/{:03d}.jpg".format(self.slides_path('big'), index))
    if resize is not None: img = cv2.resize(img, resize)
    return img[:,:,[2,1,0]]  #convert for matplotlib
