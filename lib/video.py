import cv2, cv
import collections
import numpy as np
import pandas as pd

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

  def __init__(self, stream_path=""):
    self.stream_path = stream_path

  def get_frame(self, index):
    """Return converted image for show in matplotlib
    """
    if index > self.frame_count: raise Exception("Frame index is out of range.")
    capture = cv2.VideoCapture(self.vpath)
    capture.set(cv.CV_CAP_PROP_POS_FRAMES, index)
    ret, img = capture.read()
    return img[:,:,[2,1,0]] #convert for matplotlib

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
    fin = capr['seconds'] if (end == -1 and end < capr['seconds']) else end
    iset = collections.deque([])
    while i < fin:
      cap.set(cv.CV_CAP_PROP_POS_MSEC, i*time_span)
      grabed, img = cap.read()
      if grabed:
        iset.append( dict(img=img, ms=cap.get(cv.CV_CAP_PROP_POS_MSEC)) )
        if len(iset) > size: iset.popleft()
        yield(iset)
      i = i + 1

  def get_frame(self, ms=0):
    cap = self.cap['cap']
    cap.set(cv.CV_CAP_PROP_POS_MSEC, ms)
    grabed, img = cap.read()
    return img[:,:,[2,1,0]] #convert for matplotlib

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

