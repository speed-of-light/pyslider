__doc__ = """
Perform feature matching on features
"""

__all__ = []

import cv2
from lib.exp.base import ExpCommon
from lib.exp.tools.timer import ExpTimer
from lib.exp.featx import Featx
from lib.exp.match.base import Mahelp


class Matchx(ExpCommon, Mahelp):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        # create base dir
        ExpCommon.common_path(self, "stores", asure=True)
        Mahelp.__init__(self)
        self.fx = Featx(self.root, self.name)
        self.fx.silent = True
        self.set_match_core()
        self.set_featx()

    def __klass_var(self):
        st = "{}_{}".format(self.fx.klass_var, self.mcore)
        self.klass_var = st
        self.elog.info("Current configs: {}".format(st))

    def __matching(self, matcher, sk=None, fk=None, thres=0.9):
        mra = []
        with ExpTimer(verbose=0) as ts:
            if len(fk) > 0:
                mra = matcher.knnMatch(sk.values, fk.values, k=2)
                mra = self._remove_high_simi(mra, thres)
        mdf = self._to_df(mra)
        return mdf, ts

    def __save_rtlog(self, pairs=None, lens=None, info=None):
        pairs.extend(lens)
        pairs.extend(info)
        self.save_rtlog(self._rtlog_cols(), pairs)

    def __match_info(self, mat, time, fxp):
        data = self._match_info(mat, time.msecs, fxp)
        self.elog.info(self._info_str(**data))
        self.__save_rtlog(**data)

    def __match_mem(self, **opts):
        self.matches.append(opts)

    def __match_info_mem(self, mat, time, fxp):
        """
        In memory verison of __match_info
        """
        data = self._match_info(mat, time.msecs, **fxp)
        self.elog.info(self._info_str(**data))
        self._mem_rtlog(**data)

    def __save_match(self, sid, fid, df):
        self.save(self._pair_key(sid, fid), df)

    def __match(self, sids, fids, thres=0.8):
        """
        Save matched result by `keys` formated as:
            `m_{sid:03d}_{fid:03d}`
        """
        ma = cv2.DescriptorMatcher_create(self.mcore)
        sfs = self.fx.load_slides_feats(sids)
        for fid in fids:
            fk = self.fx.load_frame_feats(fid)
            for sid, sk in zip(sids, sfs):
                fxp = dict(sk=sk, fk=fk, thres=thres)
                df, optime = self.__matching(ma, **fxp)
                fxp.update(dict(sid=sid, fid=fid))
                self.__match_info(df, optime, fxp)
                self.__save_match(sid, fid, df)

    def __match_core(self, ma, **opts):
        fxp = dict(sk=opts["sk"], fk=opts["fk"])
        df, optime = self.__matching(ma, **fxp)
        fxp.update(dict(fid=opts["fid"], sid=opts["sid"]))
        self.__match_info_mem(df, optime, fxp)
        self.__match_mem(sid=opts["sid"], fid=opts["fid"], df=df)

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

    def match(self, thres=0.8):
        sids, fids = self.seeds()
        self.__match(sids, fids, thres)

    def single_match(self, fid, thres=0.9):
        """
        Try to find matches on a single frame
        Check `self.rtlog` and `matches` as result
        """
        self.matches = []
        ma = cv2.DescriptorMatcher_create(self.mcore)
        sids = self.slide_seeds()
        sfs = self.fx.load_slides_feats(sids)
        fk = self.fx.load_frame_feats(fid)
        for sid, sk in zip(sids, sfs):
            self.__match_core(ma, thres=thres, sid=sid, fid=fid, sk=sk, fk=fk)
