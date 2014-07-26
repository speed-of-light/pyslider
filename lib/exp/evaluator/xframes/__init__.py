from base import _Base as Base
from roc_detail import RocDetail as Rocd
from scov import _Scov as Scov
from sf_cov import _SFcov as SFcov


class XframeEval(Rocd, Base):
    def __init__(self, xf):
        self.xf_ = xf
        self.preview = True
        Base.__init__(self)

    def timer(self, keys=[1, 2, 3]):
        # bs = [self.__core(k, d) for k, d in self.xf_.crossing(keys)]
        # bs = reduce(lambda x, y: x+y, bs)
        # acc = Accuracy(bs, self.preview)
        # return acc.details(acc.Common_Details+["fdr", "speficity"])
        pass

    def storages(self):
        pass

    def coverages(self, fixes=dict(pre_ns=47, pre_ws=61), keys=[]):
        scov = Scov(self.gnd, **fixes)
        return scov.compute(self.xf_.rev_crossing(keys))

    def sf_covs(self, data, fixes=dict()):
        scov = SFcov(self.gnd, **fixes)
        return scov.compute(data)
