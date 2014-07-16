from lib.exp.base import ExpCommon
from lib.exp.tools.timer import ExpTimer as ET
from conf import _Conf as Cfg
from common import _Common as Cmn


class _Base(Cfg, Cmn, ExpCommon):
    def __init__(self, root, name):
        """
        Configurations
        Common processing
        Core paring
        """
        ExpCommon.__init__(self, root, name)
        ExpCommon.common_path(self, "stores", asure=True)
        Cfg.__init__(self)
        Cmn.__init__(self)

    def __skip_info(self, frame=None, slide=None):
        nfo = "Skipped pairing since no data at {}"
        pfo = "({}, {})".format(slide["pid"], frame["pid"])
        return nfo.format(pfo)

    def __reject_dist_ratio(self, m, n):
        """
        According to wiki:
            thres: greater than 0.8, which eliminates 90% of the false matches
            while discarding less than 5% of the correct matches
        """
        if m.distance < n.distance*self.bbft:
            return m
        return None

    def __best_bin_first(self, matches):
        """
        Remove high similarity pairs
          Beis, J., and Lowe, D.G "Shape indexing using approximate nearest-
          neighbour search in high-dimensional spaces", Conference on Computer
          Vision and Pattern Recognition, Puerto Rico, 1997, pp. 1000-1006
        """
        not_non = lambda v: v is not None
        rejector = lambda (m, n): self.__reject_dist_ratio(m, n)
        return filter(not_non, map(rejector, matches))

    def __pairing_core(self, slide=None, frame=None):
        """
        frame, slide: should containing `pid`, `des`, `kps`
        """
        nnr = self.matcher.knnMatch(frame["des"].values,
                                    slide["des"].values, k=2)
        nnrl = len(nnr)
        mli = self.__best_bin_first(nnr)
        return Cmn._to_matches_df(self, mli), nnrl

    def __pairing_base(self, sx, fx):
        pin = "Pairing s-{: 3d}, f-{: 5d}"
        self.elog.info(pin.format(sx["pid"], fx["pid"]))
        dp = self._pairing(slide=sx, frame=fx)
        return dp

    def _pairing(self, slide=None, frame=None):
        data = dict(slide=slide, frame=frame)
        with ET(verbose=0) as ts:
            if len(frame["kps"]) == 0:
                self.elog.info(self.__skip_info(**data))
                pdf, odfl = [], len(data)
            else:
                pdf, odfl = self.__pairing_core(**data)
        if self.save_matches:
            self._save_pdf(pdf, **data)
        data.update(timer=ts, data=pdf, olen=odfl)
        return Cmn._statisticalize(self, **data)

    def __bp_base(self, prefx="rs", base_feats=None):
        self._update_klass_var()
        sdl = []
        for bf in base_feats:
            bpb = lambda sx: self.__pairing_base(sx, bf)
            sdl += map(bpb, self.featx.slides)
        return self._save_stats(prefx, sdl)

    def _batch_pairing(self, fs=0, fe=-1):
        self.__bp_base("rs", self.featx.frames[fs:fe])

    def _batch_slides_pairing(self, ss=0, se=-1):
        self.__bp_base("ss", self.featx.slides[ss:se])
