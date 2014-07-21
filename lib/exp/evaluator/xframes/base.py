from lib.exp.base import ExpCommon
from lib.exp.tools.preloader import Preloader as Pldr
from lib.exp.evaluator.ground_truth import GroundTruth as GT


class _Base(Pldr, ExpCommon):
    def __init__(self):
        ExpCommon.__init__(self, self.xf_.root, self.xf_.name)
        Pldr.__init__(self)
        Pldr._preload(self, "gnd")

    def _reload(self, module="gnd"):
        if module == "gnd":
            mod = GT(self.root, self.name)
        self.__dict__[module] = mod

    def cross_result(self, data, dkey="mean_ans"):
        gkey = "{}_gnd".format(dkey[:-4])
        data[gkey] = map(self.gnd.answer, data["fid"].values)

    def cross_results(self, data, dkeys=["mean"]):
        crd = lambda k: self.cross_result(data, k)
        map(crd, dkeys)
