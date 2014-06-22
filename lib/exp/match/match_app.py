from lib.exp.base import ExpCommon
from lib.exp.evaluator.ground_truth import GroundTruth
from lib.exp.match import Matchx
from lib.exp.filters.ransac import Ransac
from base import MatchBase


class MatchAppBase(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        self.__preload_ground_truth()

    def _get_matches_means(self, mat_pack):
        ys = []
        for match in mat_pack:
            df = match["df"]
            if len(df) > 0:
                y = df.dist.mean()
            else:
                y = -1
            ys.append(y)
        return ys

    def __reload_ground_truth(self):
        self.gnd = GroundTruth(self.root, self.name)

    def __preload_ground_truth(self):
        if not hasattr(self, "gnd"):
            self.__reload_ground_truth()

    def __reload_matchx(self):
        self.matchx = Matchx(self.root, self.name)
        self.matchx.silent = True

    def _preload_matchx(self):
        if not hasattr(self, "matchx"):
            self.__reload_matchx()


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
        self._preload_matchx()
        ms = []
        for fid, matches in self.matchx.batch_matches(thres=thres):
            matches = yield(matches)
            ms.append(self._get_matches_means(matches))
            self.elog.info("Match app appending fid:{}".format(fid))
        self.knnms = ms
        yield None

    def ransac_mean_pairs(self, thres=1.01):
        ky = self.knn_mean_pairs(thres=thres)
        matches = ky.next()
        while matches is not None:
            ra = Ransac(self.matchx)
            ra.filter_pairs()
            matches = ky.send(ra.new_matches())
