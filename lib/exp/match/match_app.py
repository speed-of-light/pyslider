from lib.exp.base import ExpCommon
from lib.exp.pre import Reducer


class MatchAppBase(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        pass

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
