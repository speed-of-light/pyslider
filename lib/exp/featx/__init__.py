__all__ = []

from lib.exp.base import ExpCommon


class Featx(ExpCommon):
    def __init__(self, root, name):
        """
        Collecting features from image and frames
        """
        ExpCommon.__init__(self, root, name)
        # create base dir
        ExpCommon.common_path(self, "stores", asure=True)
        self.algo = dict(kp_adap="", kp_core="SIFT",
                         des_adap="", des_core="SIFT")
        self.__klass_var()

    def set_algorithm(self, engine="keypoint", method="SIFT"):
        """
        Adaptive method for keypoints detection:
            `kp_adap`: '', 'Grid', 'Pyramid'
        Keypoints detection core:
            `kp_core`: "FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"
        Adaptive method for descriptor detection:
            `des_adap`: '', 'Opponent'
        Descriptor detection core:
            `des_core`: "SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"
        """
        self.algo[engine] = method
        self.__klass_var()

    def __klass_var(self):
        st = "{kp_adap}_{kp_core}_{des_adap}_{des_core}".\
            format(**self.algo)
        self.klass_var = st

    def make_feats(self):
        pass

    def save_feats(self):
        pass
