from lib.exp.base import ExpCommon
from lib.exp.pairing import PairFeats as Pif


class _Base(ExpCommon):
    def __init__(self, root, name, pairs=None):
        ExpCommon.__init__(self)
        if pairs:
            self.pairs = pairs

    def _get_pairs(self):
        self._preload("pairs")
        return self.pairs

    def _reload(self, module="pairs"):
        if module == "pairs":
            mod = Pif(self.root, self.name)
            mod.warmup()
        self.__dict__[module] = mod

    def _get_pair_stats(self, key=0):
        self._preload("pairs")
