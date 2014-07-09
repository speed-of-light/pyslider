from lib.exp.base import ExpCommon
from lib.exp.tools.timer import ExpTimer as ET
from preloader import _Preloader as Pldr
from conf import _Conf as Cfg
from common import _Common as Cmn


class _Base(ExpCommon, Cfg, Cmn, Pldr):
    def __init__(self, root, name):
        """
        Configurations
        Common processing
        Core paring
        """
        ExpCommon.__init__(self, root, name)
        ExpCommon.common_path(self, "stores", asure=True)
        Pldr.__init__(self)
        Cfg.__init__(self)
        Cmn.__init__(self)

    def __skip_info(self, frame=None, slide=None):
        nfo = "Skipped pairing since no data at {}"
        pfo = "({}, {})".format(slide["pid"], frame["pid"])
        return nfo.format(pfo)

    def _pairing(self, data, nn_dist=0.9):
        # NOTICE the skipped data should be re-considered
        with ET(verbose=0) as ts:
            if len(data["frame"]["kps"]) == 0:
                self.elog.info(self.__skip_info(**data))
                return None
            else:
                pdf = self.__pairing_core(nn_dist=0.9, **data)
                self._save_pdf(pdf, **data)
        return Cmn._statisticalize(self, pdf, ts, **data)

    def __pairing_core(self, frame=None, slide=None, nn_dist=0.9):
        """
        frame, slide: should containing `pid`, `des`, `kps`
        """
        nnr = self.matcher.knnMatch(frame["des"].values,
                                    slide["des"].values, k=2)
        mli = self.__best_bin_first(nnr, nn_dist)
        return Cmn._to_matches_df(self, mli)

    def __reject_dist_ratio(self, m, n, thres=0.8):
        """
        According to wiki:
            thres: greater than 0.8, which eliminates 90% of the false matches
            while discarding less than 5% of the correct matches
        """
        if m.distance < n.distance*thres:
            return m
        return None

    def __best_bin_first(self, matches, nn_dist=.9):
        """
        Remove high similarity pairs
          Beis, J., and Lowe, D.G "Shape indexing using approximate nearest-
          neighbour search in high-dimensional spaces", Conference on Computer
          Vision and Pattern Recognition, Puerto Rico, 1997, pp. 1000-1006
        """
        not_non = lambda v: v is not None
        rejector = lambda (m, n): self.__reject_dist_ratio(m, n, nn_dist)
        return filter(not_non, map(rejector, matches))
