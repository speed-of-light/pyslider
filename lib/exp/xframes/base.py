from lib.exp.base import ExpCommon
from lib.exp.tools.preloader import Preloader as Pldr
from lib.exp.tools.configurator import Configurator as Cfgr
from lib.exp.pairing import PairFeats as Pif


class _Base(Cfgr, Pldr, ExpCommon):
    _vars = ["gmmc"]

    _vals = [2]

    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)
        Pldr.__init__(self)
        Pldr._preload(self, "pairs")
        Cfgr.__init__(self)

    def _reload(self, module="pairs"):
        if module == "pairs":
            mod = Pif(self.root, self.name)
            mod.warmup()
        self.__dict__[module] = mod
