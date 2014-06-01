import numpy as np
import pandas as pd
import glob
import cv2
from ..data import PdfReader, Video
from base import ExpCommon


class Summary:
    def __init__(self):
        self.sp = 'data/store.h5'
        self.load()

    def load(self, key='summary'):
        self.sdf = pd.read_hdf(self.sp, key, format='t')
        return self.sdf

    def save(self, key='summary', data=None):
        if data is None:
            data = self.df
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
      for pn in data[['n_rootl', 'n_name']].values:
        ps = PdfReader(pn[0], pn[1])
        yield ps

    def base_info(self):
        """ collect base information into summary
        """
        data = self.summary
        for ps in self.ps_list():
            vp = glob.glob("./data/{}/{}/video.*".format(ps.root, ps.name))[0]
            vs = Video(vp)
            vsc = vs.cap
            rv = data[data.n_name == ps.name].index.values
            data['n_time'][rv] = int(vsc['seconds'])
            data['n_frames'][rv] = int(vsc['frames'])
            if ps.pages is None:
                imgroot = "./data/{}/{}/slides".format(ps.root, ps.name)
                imgs = glob.glob1(imgroot, "*.jpg")
                data['n_slides'][rv] = len(imgs)
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
                if ps.pages is None:
                    continue
                ps.to_jpgs(size=si)
                print ps.pdf_path

    def mark_table(self, key, columns, values):
        """ Mark generated data for specific talk
        :key: data key
        :values: array that contained with (talk, existed) pair
        """
        sda = self.summary
        cols = sda.columns if columns is None else columns
        data = sda[sda.n_name.isin([c for c in cols])]
        print len(data)
        for v in data[['n_name', 'n_root']].values:
            print v


class Slider(ExpCommon):
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
