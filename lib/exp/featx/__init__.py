__all__ = []

from lib.exp.base import ExpCommon


class Featx(ExpCommon):
    def __init__(self, root, name):
        """
        Collecting features from image and frames
        """
        ExpCommon.__init__(self, root, name)
        self.algo = dict(keypoint="SIFT", descriptor="SIFT")

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

    def make_feats(self):
        pass

    def save_feats(self):
        pass
