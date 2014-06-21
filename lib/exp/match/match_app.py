from lib.exp.base import ExpCommon
from lib.exp.pre import Reducer
from lib.exp.evaluator.ground_truth import GroundTruth


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
