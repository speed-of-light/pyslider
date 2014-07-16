import cv2
from lib.exp.featx import Featx
from lib.exp.tools.preloader import Preloader as Pldr
from lib.exp.tools.configurator import Configurator as Cfgr


class _Conf(Cfgr, Pldr):
    _vars = ["bbft", "ransac", "homo",
             "octaf", "save_matches"]

    _vals = [0.9, None, False,
             0, False]

    def __init__(self):
        # bbft: distance
        # ransac: px torlerance
        # homo: homo negative weight
        # vals: consider only normal frame, 0 forall
        Pldr.__init__(self)
        Cfgr.__init__(self)

    def set_featx(self, preload=True, kp="SIFT", des="SIFT"):
        self.elog.info("Loading featx")
        Pldr._preload(self, "featx")
        self.featx.preset(kp, des)
        self.featx.preload_packs(preload)

    def set_matcher(self, fn="FlannBased"):
        """
        BruteForce BruteForce-L1
        BruteForce-Hamming BruteForce-Hamming(2)
        FlannBased
        """
        self.elog.info("Loading matcher")
        self.mcore = fn
        self._reload("matcher")

    def _reload(self, mod="matcher"):
        print "override reloading {}".format(mod)
        if mod == "matcher":
            _mod = cv2.DescriptorMatcher_create(self.mcore)
        elif mod == "featx":
            _mod = Featx(self.root, self.name)
        self.__dict__[mod] = _mod
