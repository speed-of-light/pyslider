from base import _Base as Base
from roc_detail import RocDetail as Rocd


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