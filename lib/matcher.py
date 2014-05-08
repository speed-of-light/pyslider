import cv2, cv
import collections, os
import numpy as np
import pandas as pd
import glob, os.path
from lib._exp.fetus import Summary
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
