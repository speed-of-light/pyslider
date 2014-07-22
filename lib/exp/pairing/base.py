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

    def __sinfo_log(self, sx=None, fx=None):
        nfo = "Skipped pairing since no data at {}"
        pfo = "({}, {})".format(sx["pid"], fx["pid"])
        self.elog.info(nfo.format(pfo))

    def __pinfo_log(self, sid, fid):
        pin = "Pairing s-{: 3d}, f-{: 5d}"
        self.elog.info(pin.format(sid, fid))

    def __pairing_base(self, sx, fx):
        self.__pinfo_log(sx["pid"], fx["pid"])
        dp = self.__pair_without_null(slide=sx, frame=fx)
        return dp

    def __pairing_core(self, sx=None, fx=None):
        """
        frame, slide: should containing `pid`, `des`, `kps`
        """
        nnr = self.matcher.knnMatch(sx["des"].values, fx["des"].values, k=2)
        nnrl = len(nnr)
        mdf = self.pcore.pairing(nnr, sx, fx)
        return mdf, nnrl

    def __pair_without_null(self, slide=None, frame=None):
        data = dict(sx=slide, fx=frame)
        with ET(verbose=0) as ts:
            if len(frame["kps"]) == 0:
                self.__sinfo_log(**data)
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
        self._save_stats(prefx, sdl)

    def _batch_pairing(self, fs=0, fe=None):
        self.__bp_base("rs", self.featx.frames[fs:fe])

    def _batch_slides_pairing(self, ss=0, se=None):
        self.__bp_base("ss", self.featx.slides[ss:se])
