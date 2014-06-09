import cv2
import pandas as pd
import numpy as np
import itertools
from base import ExpCommon
from tools.timer import ExpTimer
from tools.slider import Slider
from summary import Summary


class Feats(ExpCommon, Slider):
    def __init__(self, root, name):
        """
        """
        ExpCommon.__init__(self, root, name)

    def __str__(self, mn=None):
        ret = "{}[{}]".format(self.root, self.name)
        if mn is not None:
            ret += " - {}".format(mn)
        return ret

    def _df_key_root(self, mod, opt, set_name='slide', dtype='kp'):
        hdfk = "/{}/{}".format(mod['kp_algo'], mod['des_algo'])
        us = self._ustr_dict(opt)
        fik = "{}{}/{}/{}".format(hdfk, us, set_name, dtype)
        return fik

    def __set_value(self, exc, name, value):
        dtype = exc.paramType(name)
        if dtype == 0 or dtype == 10:
            exc.setInt(name, int(value))
        elif dtype == 1:
            exc.setBool(name, bool(value))
        elif dtype == 2:
            exc.setDouble(name, float(value))
        elif dtype == 3:
            exc.setString(name, str(value))

    def _set_extractor(self, exc, opts={}):
        for dk in opts.keys():
            self.__set_value(exc, dk, opts[dk])
        if 0:
            for p in exc.getParams():
                res = self._get_exc_value(exc, p)
                print p, res

    def _get_exc_value(self, exc, name):
      dtype = exc.paramType(name)
      if dtype == 0 or dtype == 10:
          v = exc.getInt(name)
      elif dtype == 1:
          v = exc.getBool(name)
      elif dtype == 2:
          v = exc.getDouble(name)
      elif dtype == 3:
          v = exc.getString(name)
      va = ['Int', 'Bool', 'Double', 'Str', '-', '-', '-', '-',
            '-', '-', 'Short']
      return (va[dtype], v)

    def _unpickle_keypoints(self, kdf):
      if kdf is None:
          return None
      kps = []
      for ki in kdf.index:
        kd = kdf.ix[ki]
        ktmp = cv2.\
            KeyPoint(x=kd['x'], y=kd['y'],
                     _size=kd['size'], _angle=kd['angle'],
                     _response=kd['response'], _octave=int(kd['octave']),
                     _class_id=int(kd['class_id']))
        kps.append(ktmp)
      return kps

    def o_frames(self, gray=False):
      pass

    def o_slides(self, gray=False, resize=None):
        """
        Get slide images collection
        """
        spm = self.slides_path(size='big')
        su = Summary()
        sin = su.info(self.root, self.name)
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        for si in range(1, sin.n_slides+1):
            sp = "{}/{:03d}.jpg".format(spm, si)
            if gray:
                img = cv2.imread(sp, cv2.COLOR_GRAY2BGR)
            else:
                img = cv2.imread(sp)
            if resize is not None:
                img = cv2.resize(img, resize)
            yield(dict(img=img, idx=si))

    def comb_fm_list(self):
      """
      List combinations of each methods
      """
      kp_adp = ['', 'Grid', 'Pyramid']
      kp_algo = ["FAST", "FASTX", "STAR", "SIFT", "SURF",
                 "ORB", "MSER", "GFTT", "HARRIS"]
      kps = [dd[0]+dd[1] for dd in itertools.product(kp_adp, kp_algo)]
      des_adp = ['', 'Opponent']
      des_algo = ["SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"]
      des = [dd[0]+dd[1] for dd in itertools.product(des_adp, des_algo)]
      pkg = [dd for dd in itertools.product(kps, des)]
      return pkg

    def detect_with(self, img_iter=[], img_type='slide',
                    mod=dict(kp_algo='FAST', des_algo='SIFT'), **opts):
        """
        `mod` dict should include
          `kp_adp`: '', 'Grid', 'Pyramid' #adaptive method for detection
          `kp_algo`: "FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"
          `des_adp`: '', 'Opponent'
          `des_algo`: "SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"
        """
        fd = cv2.FeatureDetector_create(mod['kp_algo'])
        de = cv2.DescriptorExtractor_create(mod['des_algo'])
        # if det.empty(): return None
        cols = ['x', 'y', 'size', 'angle', 'response', 'octave', 'class_id']
        dkrk = self._df_key_root(mod, opts, img_type)
        dkrd = self._df_key_root(mod, opts, img_type, dtype='desc')
        dlog = pd.DataFrame(columns=['ms', 'kps']).convert_objects()
        self.elog.info("param path => " + dkrk)
        for im in img_iter:
            idx = im['idx']
            img = im['img']
            with ExpTimer(verbose=0) as ts:
                kps = fd.detect(img, None)
                kps, des = de.compute(img, kps)
            data = [[kp.pt[0], kp.pt[1], kp.size, kp.angle,
                    kp.response, kp.octave, kp.class_id] for kp in kps]
            kdf = pd.DataFrame(data, columns=cols)
            ddf = pd.DataFrame(des)
            kdf[kdf.columns] = kdf[kdf.columns].astype(kdf['x'].dtype)
            ddf.columns = [("i_" + str(cc)) for cc in ddf.columns]
            self.save("{}/i{:03d}".format(dkrk, idx), kdf)
            self.save("{}/i{:03d}".format(dkrd, idx), ddf)
            llog = pd.DataFrame([[int(ts.msecs), len(des)]],
                                columns=['ms', 'kps'])
            dlog = dlog.append(llog)
            logstr = self.__str__("sid[{}] ".format(idx)) + str(ts.msecs)
            self.elog.info(logstr)
        dklg = self._df_key_root(mod, opts, img_type, dtype='log')
        dlog = dlog.reset_index()
        del dlog['index']
        dlog[dlog.columns] = dlog[dlog.columns].astype(np.uint32)
        self.save(dklg, dlog)
        self.elog.info("fn finished" + dkrk)
        return dlog

    def run_all_slides(self, np=''):
        cfl = self.comb_fm_list()
        with ExpTimer() as ts:
            for cc in cfl:
                osl = self.o_slides(gray=('Opponent' not in cc[1]))
                try:
                    self.\
                        detect_with(img_iter=osl, img_type='slide',
                                    mod=dict(kp_algo=cc[0], des_algo=cc[1]))
                except Exception as e:
                    self.log.error("<<{}-{}>>: {}".format(cc[0], cc[1], e))
                    continue
        self.notify("Time: {}".format(ts.tstr()))

    def detect_match_with(self, fr_list=[],
                          mod=dict(kp_algo='FAST', des_algo='SIFT')):
        """
        Detect and find best matched result from slides results
        """
        fd = cv2.FeatureDetector_create(mod['kp_algo'])
        de = cv2.DescriptorExtractor_create(mod['des_algo'])
        for im in fr_list:
            # iid = im['index']
            img = im['img']
            with ExpTimer(verbose=0) as ts:
                kps = fd.detect(img, None)
                kps, des = de.compute(img, kps)
            ts.msecs

    def resrc(self):
        """
        http://docs.opencv.org/trunk/doc/py_tutorials/
          py_feature2d/py_fast/py_fast.html
        sift http://opencv-python-tutroals.readthedocs.org/
          en/latest/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html
        surf http://opencv-python-tutroals.readthedocs.org/
          en/latest/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html?highlight=surf
        brisk http://docs.opencv.org/trunk/modules/features2d/
          doc/feature_detection_and_description.html
        """
        pass

    def load_feats(self,
                   mod=dict(kp_algo='FAST', des_algo='SIFT')):
        su = Summary()
        sin = su.info(self.root, self.name).iloc[0]
        ns = sin.n_slides
        key_root = "/{kp_algo}/{des_algo}/slide".format(**mod)
        sfd = []
        for si in range(1, ns+1):
            kk = key_root + "/kp/i{:03d}".format(si)
            dk = key_root + "/desc/i{:03d}".format(si)
            kps = self._unpickle_keypoints(self.load(kk))
            des = self.load(dk)
            des = None if des is None else des.values
            sfd.append(dict(idx=si, kps=kps, des=des))
        return sfd

    def feats_set(self, ilist=[],
                  mod=dict(kp_algo='FAST', des_algo='SIFT')):
        """self.o_slides(gray=True, resize=True)
        """
        fd = cv2.FeatureDetector_create(mod['kp_algo'])
        de = cv2.DescriptorExtractor_create(mod['des_algo'])
        res = []
        for si in ilist:
            img = si['img']
            with ExpTimer(verbose=0) as ts:
                ks = fd.detect(img)
                ks2, ds = de.compute(img, ks)
            res.append(dict(idx=si['idx'], kps=ks2, des=ds,
                       kplen=len(ks), ts=ts.msecs))
        return res

    def single_feats(self, img,
                     mod=dict(kp_algo='FAST', des_algo='SIFT')):
        fd = cv2.FeatureDetector_create(mod['kp_algo'])
        de = cv2.DescriptorExtractor_create(mod['des_algo'])
        ks = fd.detect(img)
        ks, ds = de.compute(img, ks)
        return ks, ds
