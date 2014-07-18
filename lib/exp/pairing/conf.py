import cv2
from lib.exp.featx import Featx
from lib.exp.tools.preloader import Preloader as Pldr
from lib.exp.tools.configurator import Configurator as Cfgr
from ext import _Core as Core


class _Conf(Cfgr, Pldr):
    # Update here should also update implementationnote too
    _conf = dict(
        bbft=0.9, thres=0, homo=False, mm=10, area=True,
        invw=0, octaf=0, save_matches=False)

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

    def _configs(self):
        dp = dict(
            root=self.root, name=self.name,
            bbft=self.bbft, thres=self.thres, homo=self.homo,
            mm=self.mm, area=self.area, invw=self.invw, octaf=self.octaf)
        return dp

    def _reload(self, mod="matcher"):
        print "override reloading {}".format(mod)
        if mod == "matcher":
            _mod = cv2.DescriptorMatcher_create(self.mcore)
        elif mod == "featx":
            _mod = Featx(self.root, self.name)
        elif mod == "pcore":
            _mod = Core(**self._configs())
        self.__dict__[mod] = _mod

    def ImplementationNotes(self):
        print "bbft:", "nearest neighbor threshold"
        print "ransac", "ransac threshold"
        print "ranmin", "min feature points to running ransac"
        print "harea", "Considering homo area"
        print "inv_homow", "use inverse weight for points in homography"
        print "octaf", "use one layer octaf of keypoints"
        print "save_matches", "slow down the whole process"
