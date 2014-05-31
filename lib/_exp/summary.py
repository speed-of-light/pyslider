import numpy as np
import pandas as pd
import glob
from ..data import PdfSlider, Video


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
      for pn in data[['n_name', 'n_root']].values:
        ps = PdfSlider(pn[0], pn[1])
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
