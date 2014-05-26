from matplotlib import offsetbox as ofb
import math
import cv2
import pandas as pd
import numpy as np
from sklearn import mixture
from summary import Summary
from feats import Feats
from ..data import Video, PdfSlider
from ..handy import HandyTimer as ht
from ..exp import ExpCommon


class Ransac():
    def __init__(self):
      pass

    def _matched_points(self, kps, mps):
      rr = [kps[m].pt for m in mps]
      return np.float32(rr).reshape(-1, 1, 2)

    def compute(self, data, min_matches=10):
        """
        data is a dict contained columns:
        [ 'kp_train', 'kp_test', 'matches']
        Methods:
          0 - a regular method using all the points
          CV_RANSAC - RANSAC-based robust method
          CV_LMEDS - Least-Median robust method
        """
        good = data['matches']
        kpq = data['sif']['kps']
        kpt = data['vif']['kps']
        if len(good) >= min_matches:
          qpts = self._matched_points(kpq, good.qix)
          tpts = self._matched_points(kpt, good.tix)
          M, mask = cv2.findHomography(qpts, tpts, method=cv2.RANSAC,
                                       ransacReprojThreshold=5.0)
          return M, mask
        return None

    def get_bound_img(self, fid, sid, homo):
        """
        Return homographic array of image result
        Params:
            fid: id of frames
            sid: id of slide
            homo: transformation matrix (usually 9*9)
        """
        fimg, simg = self._image_pair(fid, sid)
        h, w, z = fimg.shape
        bnd = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]). \
            reshape(-1, 1, 2)
        bound = cv2.perspectiveTransform(bnd, homo)
        rimg = cv2.polylines(simg, [np.int32(bound)], True, (0, 255, 0), 3)
        return rimg


class Matcher(ExpCommon):
    def __init__(self, root, name):
      """
      Get effective frame lists from prepared data
      """
      ExpCommon.__init__(self, root, name)

    def _match_info(self, sid, fid, kalg, dalg, mtype, thres):
      rs = "sid:{}, fid:{}, mod:{}-{}, mtype:{},thres:{}" \
           .format(sid, fid, kalg, dalg, mtype, thres)
      return rs

    def set_match(self, fids=[], mtype="BruteForce", thres=.9,
                  mod=dict(kp_algo='FAST', des_algo='SIFT')):
      sr = self.root
      sn = self.name
      ff = Feats(sr, sn)
      isl = ff.o_slides(gray=True, resize=True)
      vv = Video(sr, sn)
      ivl = vv.get_frames(ids=fids, gray=True)
      sfs = ff.feats_set(isl, mod=mod)
      vfs = ff.feats_set(ivl, mod=mod)
      res = []
      for qf in vfs:
        frs = []
        for tf in sfs:
          _info = self._match_info(tf['idx'], qf['idx'], mod['kp_algo'],
                                   mod['des_algo'], mtype, thres)
          self.log.info(_info)
          with ht(verbose=0) as ts:
            mr = self._match_desc(qf['des'], tf['des'], mtype, thres)
            mt = ts.msecs+tf['ts']+qf['ts']
            dr = dict(sid=tf['idx'], fid=qf['idx'], ts=mt, mr=mr)
            frs.append(dr)
            ds = self._dist_stat(frs)
            vr = self._voting(ds)
            res.append(dict(feats=frs, vr=vr))
            return res, sfs, vfs

    def _match_desc(self, dquery, dtrain, mtype="BruteForce", thres=.5):
        """
        BruteForce-L1 BruteForce-Hamming BruteForce-Hamming(2) FlannBased
        """
        mat = cv2.DescriptorMatcher_create(mtype)
        # mre = mat.match(dquery, dtrain)
        mra = mat.knnMatch(dquery, dtrain, k=2)
        mre = []
        for m, n in mra:
          if m.distance < n.distance*thres:
            mre.append(m)
            mra = []
            for re in mre:
              mra.append([re.queryIdx, re.trainIdx, re.imgIdx, re.distance])
              if len(mra) is 0:
                return pd.DataFrame(columns=['qix', 'tix', 'iix', 'dt'])
              else:
                return pd.DataFrame(mra, columns=['qix', 'tix', 'iix', 'dt'])

    def _filter_matches(self, matches, thres=.5):
      mre = []
      for m, n in matches:
        if m.distance < n.distance*thres:
          mre.append(m)
          return mre

    def _pickle_matches(self, matches):
      mra = []
      for m in matches:
        mra.append([m.queryIdx, m.trainIdx, m.imgIdx, m.distance])
        return mra

    def _image_pair(self, fid, sid):
      sr = self.root
      sn = self.name
      vv = Video(sr, sn)
      fi = vv.get_frames([fid]).next()
      ss = PdfSlider(sn, sr)
      si = ss.get_slides([sid], gray=True, resize=True).next()
      return fi, si

    def single_match(self, fid, sid, mtype="BruteForce",
                     mod=dict(kp_algo='FAST', des_algo='SIFT')):
        """
        BruteForce-L1 BruteForce-Hamming BruteForce-Hamming(2) FlannBased
        """
        fimg, simg = self._image_pair(fid, sid)
        ff = Feats(self.root, self.name)
        sif = ff.feats_set([simg], mod=mod)[0]
        vif = ff.feats_set([fimg], mod=mod)[0]
        mat = cv2.DescriptorMatcher_create(mtype)
        mra = mat.knnMatch(sif['des'], vif['des'], k=2)
        mra = self._filter_matches(mra, .9)
        col = ['qix', 'tix', 'iix', 'dt']
        if len(mra) is 0:
          res = pd.DataFrame(columns=col)
        else:
          mra = self._pickle_matches(mra)
          res = pd.DataFrame(mra, columns=col)
          return dict(matches=res, sif=sif, vif=vif)

    def _voting(self, df):
      vk = []
      for cc in df.columns:
        if cc in ['sid', 'fid']:
          continue
        vr = df[df[cc].eq(df[cc].min())]
        if len(vr) > 0:
          vk.append(int(vr.iloc[0].sid))
        else:
          vk.append(None)
          return vk

    def _dist_stat(self, fres):
      ary = []
      for fk in fres:
        mr = fk['mr']
        m3 = mr[mr.dt.gt(mr.dt.quantile(.9))].dt.mean()
        mm = mr[mr.dt.lt(mr.dt.quantile(.8)) &
                mr.dt.gt(mr.dt.quantile(.2))].dt.mean()
        m1 = mr[mr.dt.lt(mr.dt.quantile(.1))].dt.mean()
        M = mr.dt.max()
        m = mr.dt.min()
        ary.append([fk['fid'], fk['sid'], m3, mm, m1, m1/m3, M, m, m/M])
        cols = ['fid', 'sid', 'm3', 'mm', 'm1', 'm31', 'M', 'm', 'mM']
        return pd.DataFrame(ary, columns=cols)

    def _plot_match(self, qimg, qkp, timg, tkp, match):
      h1, w1 = qimg.shape[:2]
      h2, w2 = timg.shape[:2]
      view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
      view[:h1, :w1] = qimg
      view[:h2, w1:] = timg
      for mi in match.index:
        tix = int(match.ix[mi]['tix'])
        qix = int(match.ix[mi]['qix'])
        color = tuple([np.random.randint(0, 255) for _ in xrange(3)])
        qmp = (int(qkp[qix].pt[0]), int(qkp[qix].pt[1]))
        tmp = (int(tkp[tix].pt[0] + w1), int(tkp[tix].pt[1]))
        cv2.line(view, qmp, tmp, color)
        return view

    def _plot_single_match(self, fid, fkp, sid, skp, mresult):
      vv = Video(self.root, self.name)
      fimg = vv.get_frames(ids=[fid]).next()['img']
      spm = self.slides_path(size='big')
      simg = cv2.imread('{}/{:03d}.jpg'.format(spm, sid))
      su = Summary()
      sin = su.info(self.root, self.name).iloc[0]
      simg = cv2.resize(simg, (sin.v_width, sin.v_height))
      vimg = self.plot_match(fimg, fkp, simg, skp, mresult)
      return vimg
    # cv2.imwrite('jpg/test.jpg', vimg)

    def _reorder(self, old, li=[]):
        """
        Generate reordered list
        ex:
          aa= [9,3,6]; li = [1,0,0,0,0,2,0,1]
          by product: bb = { 0: 1, 1:2, 2:0}
          return: [2, 1, 1, 1, 1, 0, 1, 2]
        """
        tmp = old[:]
        tmp.sort()
        bb = {}
        for i, t in enumerate(tmp):
          bb[i] = old.index(t)
          return [bb[ll] for ll in li]

    def _basic_result(self, data, mm=2):
      clf = mixture.GMM(n_components=mm, covariance_type='full')
      clf.fit(data)
      pr = clf.predict(data)
      return np.array(self._reorder(clf.means_.tolist(), pr))

    def regroup(self, df, smres):
        """
        `df` Ground-truths dataframe, columns are:
        'fid', 'sid', 'slide_type', 'cam_status'
        `smres` Comes from method set_match and its res value
        """
        hita = []
        for r in smres:
          fid = r['feats'][0]['fid']  # 0 is ok, all the same
          qry = df[(df['fid'] <= fid)]
          if len(qry) > 0:
            qv = qry.values[-1][1]
            mr = r['feats'][qv-1]['mr']
            tmean = mr[mr.dt.lt(mr.dt.quantile(.1))].dt.mean()
            if qv > 0:  # has sid
              hita.append([fid, qv, r['vr'], tmean, None, tmean])
            elif len(r['feats'][qv-1]['mr']) > 0:  # has matched result
              hita.append([fid, qv, r['vr'], None, tmean, tmean])
            else:
              print 'never goes here'
              hitf = pd.DataFrame(hita,
                                  columns=['fid', 'sid', 'vr', 'hit',
                                           'nonhit', 'hita'])
              hitf = hitf.set_index('fid')
              hitf['pr'] = self._basic_result(hitf.hita.values, 2)
              return hitf
         # self.plot_hitf(hitf,
         #         show=[1482, 16427, 28957, 35469, 46755, 47461,66385,70360])

    # binary
    def tmp(self):
        """
        http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/
          py_feature2d/py_brief/py_brief.html?highlight=brief
        http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/
          py_feature2d/py_orb/py_orb.html?highlight=orb
        http://stackoverflow.com/questions/20146570/opencv-python-dense-sift
        http://stackoverflow.com/questions/14588682/
          freak-descriptor-with-opencv-python
        def color_hist(self):
        def text_region(self):
        http://answers.opencv.org/question/19015/how-to-use-mser-in-python/
        https://opencv-code.com/tutorials/
          automatic-perspective-correction-for-quadrilateral-objects/
        """
        pass

    def ransac(self, fid, sid, res, plot=False):
      ra = self.Ransac()
      if plot:
        fimg, simg = self._image_pair(fid, sid)
      else:
        ra.compute()

    def plot_hitf(self, data, show=[], predict=False, hints=False):
        """
        data(dataframe) should contain columns:
        ['fid', 'sid', 'vr', 'hit', 'nonhit', 'hita']
        vr: voted result ( not necessary)
        hit: similarity or confidence for true
        nonhit: similarity or confidence for false(wrong match)
        hita: combined hit and nonhit result withou nan/none
        """
        mp = self.Plotter(self.root, self.name)
        mp.plot_matches(data, show=show, predict=predict, hints=hints)

    def plot_ransac(self, ):
        pass

    class Plotter():
        def __init__(self, root, name):
          self.root = root
          self.name = name

        def _stich_imgs(self, left, right):
          h1, w1 = left.shape[:2]
          h2, w2 = right.shape[:2]
          view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
          view[:h1, :w1] = left
          view[:h2, w1:] = right
          return view

        def _ano_img_box(self, ax, vimg, simg, hitc, sid):
          hv = 0 if math.isnan(hitc.hit) else hitc.hit
          hv = hv if math.isnan(hitc.nonhit) else hitc.nonhit
          sip = 0.1 if sid % 2 is 0 else 0.9
          stimg = self._stich_imgs(simg, vimg[:, :, [2, 1, 0]])
          oft = ofb.OffsetImage(stimg, zoom=0.1)
          ab = ofb. \
              AnnotationBbox(oft, (hitc.name, hv), xycoords='data',
                             xybox=(hitc.name, sip),
                             boxcoords=("data", "axes fraction"),
                             bboxprops=dict(boxstyle='round,pad=0.1', ec='g'),
                             arrowprops=dict(arrowstyle="->", color='g'))
          ax.add_artist(ab)

        def _ano_fid_note(self, ax, hitf):
          hM = hitf['hit'].max()
          for fid in hitf.index:
            hv = hitf.ix[fid].hit  # and hitf.ix[fid].nonhit
            hva = hM*(fid % 5)*0.05
            hva = hva if fid % 2 is 0 else -hva
            oft = ofb.TextArea("{}[{}]".format(fid, hitf.ix[fid].sid))
            ab = ofb.AnnotationBbox(oft, (fid, hv), xycoords='data',
                                    xybox=(fid, hv+hva), boxcoords=("data"),
                                    bboxprops=dict(boxstyle='round,pad=0.1',
                                                   ec='g'),
                                    arrowprops=dict(arrowstyle="->",
                                                    color='darkblue'))
            ax.add_artist(ab)

        def _add_range_span(self, ax, mean, std, xpos, color='g'):
          ax.axhline(mean)
          ax.axhspan(mean-std, mean+std, facecolor=color, alpha=0.5)
          font = dict(family='serif', color='blue', weight='normal', size=16)
          ax.text(xpos, mean+3, "{:.3f}".format(mean), fontdict=font)

        def plot_matches(self, data, **kwargs):
          """
          data(dataframe) should contain columns:
          ['fid', 'sid', 'vr', 'hit', 'nonhit', 'hita']
          vr: voted result ( not necessary)
          hit: similarity or confidence for true
          nonhit: similarity or confidence for false(wrong match)
          hita: combined hit and nonhit result withou nan/none
          """
          hints = kwargs['hints']
          show = kwargs['show']
          predict = kwargs['predict']
          # Hit
          hhs = data[data['hit'].notnull()].hit
          ax = hhs.plot(style='go', figsize=(18, 9), alpha=0.6)
          self._add_range_span(ax, hhs.mean(), hhs.std(),
                               data.index.max()*0.01, color='limegreen')
          if hints:
            self._ano_fid_note(ax, data[data['hit'].notnull()])
          # Not hit
          hhs = data[data['nonhit'].notnull()].nonhit
          ax = hhs.plot(style='rx')
          self._add_range_span(ax, hhs.mean(), hhs.std(),
                               data.index.max()*0.01, color='pink')
          # Predicted
          if predict:
            hhs = data[(data.pr == 0)].hita
            ax = hhs.plot(ms=15, color='#7CFC00', ls='', marker='p', alpha=.3)
            hhs = data[(data.pr == 1)].hita
            ax = hhs.plot(ms=15, color='#ff69b4', ls='', marker='h', alpha=.3)
            # Others
            if len(show) > 0:
              vid = Video(self.root, self.name)
              slid = PdfSlider(self.name, self.root)
              for si, fi in enumerate(show):
                vimg = vid.get_frames([fi]).next()['img']
                simg = slid.get_slide(data.ix[fi].sid, resize=True)
                self._ano_img_box(ax, vimg, simg, data.ix[fi], si)
                return ax
