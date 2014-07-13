from lib.exp.base import ExpCommon
from lib.exp.tools.preloader import Preloader as Pldr
from ground_truth import GroundTruth as GT


class XframeEval(Pldr, ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        Pldr._preload(self, "gnd")

    def _reload(self, module="gnd"):
        if module == "gnd":
            mod = GT(self.root, self.name)
        self.__dict__[module] = mod

    def cross_result(self, data, dkey="mean"):
        akey = "{}_ans".format(dkey)
        gkey = "{}_gns".format(dkey)
        data[gkey] = map(self.gnd.answer, data["fid"].values)

    def cross_results(self, data, dkeys=["mean"]):
        crd = lambda k: self.cross_result(data, k)
        map(crd, dkeys)
