__all__ = []

import cv2
from lib.exp.base import ExpCommon
from lib.exp.tools.timer import ExpTimer


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
        st = "{kp_adap}{kp_core}_{des_adap}{des_core}".\
            format(**self.algo)
        self.klass_var = st

    def __engine_parts(self):
        """
        Return opencv keypoints detection and recognition parts
        """
        fdc = self.algo["kp_adap"] + self.algo["kp_core"]
        ddc = self.algo["des_adap"] + self.algo["des_core"]
        fd = cv2.FeatureDetector_create(fdc)
        de = cv2.DescriptorExtractor_create(ddc)
        return fd, de

    def __dataframe(self, kps, des):
        data = []
        cols = ["x", "y", "size", "angle", "response", "octave", "class_id"]
        for kp in kps:
            data.append([kp.pt[0], kp.pt[1], kp.size, kp.angle,
                kp.response, kp.octave, kp.class_id])
        kdf = pd.DataFrame(data, columns=cols)
        ddf = pd.DataFrame(des)
        # uniform dataframe configs
        kdf[kdf.columns] = kdf[kdf.columns].astype(kdf["x"].dtype)
        ddf.columns = [("d" + str(cc)) for cc in ddf.columns]
        return kdf, ddf

    def __featuring(self, feng, deng, imdict):
        """
        Compute and return feature data of one input image
        `feng`: feature detection engine
        `deng`: descriptor detection engine
        `imdict`: image data dictionary
        """
        with ExpTimer(verbose=0) as ts:
            kps = fd.detect(img, None)
            kpe, des = de.compute(img, kps)

        sinfo = "img: {}, kps: {}, kpe: {}, time: {}".\
            format(imdict["idx"], ts.msecs, len(kps), len(kpe))
        self.elog.info(sinfo)
        return df

    def make_feats(self, prefix="f", imgs):
        """
        prefix: `f` represents frame id
        """
        fd, dd = self.__engine_parts()
        for imd in imgs:
            df = self.__featuring(fd, dd, imd)
        pass

    def save_feats(self):
        pass
