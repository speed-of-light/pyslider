__doc__ = """
Perform feature matching on features
"""

__all__ = []

from lib.exp.base import ExpCommon
from lib.exp.featx import Featx
from base import MatchBase
from preloader import Preloader
from match_app import MatchAppBase


class Matchx(ExpCommon, MatchBase, Preloader):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        # create base dir
        ExpCommon.common_path(self, "stores", asure=True)
        MatchBase.__init__(self)
        self.fx = Featx(self.root, self.name)
        self.fx.silent = True
        self.set_match_core()
        self.set_featx()

    def __klass_var(self):
        st = "{}_{}".format(self.fx.klass_var, self.mcore)
        self.klass_var = st
        self.elog.info("Current configs: {}".format(st))

    def __save_rtlog(self, pairs=None, lens=None, info=None):
        pairs.extend(lens)
        pairs.extend(info)
        self.save_rtlog(self._rtlog_cols(), pairs)

    def __save_match(self, sid, fid, df):
        self.save(self._pair_key(sid, fid), df)

    def __match_info(self, mat, time, fxp):
        data = self._match_info(mat, time.msecs, fxp)
        self.elog.info(self._info_str(**data))
        self.__save_rtlog(**data)

    def __match_info_mem(self, mat, time, fxp):
        """
        In memory verison of __match_info
        """
        data = self._match_info(mat, time.msecs, **fxp)
        self.elog.info(self._info_str(**data))
        self._mem_rtlog(**data)

    def __match_core(self, ma, **opts):
        fxp = dict(sdes=opts["sdes"], fdes=opts["fdes"])
        df, optime = self._matching(ma, **fxp)
        fxp.update(dict(fid=opts["fid"], sid=opts["sid"]))
        self.__match_info_mem(df, optime, fxp)
        self._match_mem(sid=opts["sid"], fid=opts["fid"], df=df)

    def set_featx(self, engine="keypoint", method="SIFT"):
        """
        Refer to Featx.set_algorithm for more info
        """
        self.fx.set_algorithm(engine, method)
        self.__klass_var()

    def set_match_core(self, fn="FlannBased"):
        """
        BruteForce BruteForce-L1
        BruteForce-Hamming BruteForce-Hamming(2)
        FlannBased
        """
        self.mcore = fn
        self.elog.info("Use matching core: {}".format(fn))
        self.__klass_var()

    def frame_matches(self, fid, thres=0.9, auto_save=True):
        """
        Try to find matches on a single frame
        Check `self.rtlog` and `matches` as result
        """
        self.matches = []
        Preloader._preload(self)
        fdes = self.fx.load_frame_des(fid)
        for sid, sdes in enumerate(self.sfx, 1):
            self.__match_core(self.get_matcher(), thres=thres,
                              sid=sid, fid=fid, sdes=sdes, fdes=fdes)
        if auto_save:
            self.batch_save()

    def batch_matches(self, thres=0.8, save=False):
        """
        All frame matches iterator
        """
        fids = self.frame_seeds()
        for fid in fids:
            self.frame_matches(fid, auto_save=save)
            yield fid, self.matches

    def pair_matches(self, sid, fid, thres=0.85):
        """
        Return slide frame pairs match data
        """
        self.matches = []
        Preloader._preload(self)
        sdes = self.sfx[sid-1]
        fdes = self.fx.load_frame_des(fid)
        self.__match_core(self.get_matcher(), thres=thres,
                          sid=sid, fid=fid, sdes=sdes, fdes=fdes)

    def old_match(self, thres=0.8):
        """
        Deprecated, too slow
        """
        sids, fids = self.seeds()
        self._match(sids, fids, thres)


class MatchApp(MatchAppBase, MatchBase):
    def __init__(self, root, name):
        MatchAppBase.__init__(self, root, name)
        MatchAppBase.silent = True
        self.gnd.silent = True
        MatchBase.__init__(self)

    def knn_ms(self):
        if not hasattr(self, "knnms"):
            self.knn_mean_pairs()
        return self.knnms

    def knn_mean_pairs(self, thres=0.85):
        mm = Matchx(self.root, self.name)
        mm.silent = True
        ms = []
        for fid, matches in mm.batch_matches(thres=thres):
            ms.append(self._get_matches_means(matches))
            self.elog.info("Match app appending fid:{}".format(fid))
        self.knnms = ms
        self.matchx = mm
        return ms
