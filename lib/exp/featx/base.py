import cv2
import pandas as pd
from lib.exp.base import ExpCommon
from lib.exp.tools.timer import ExpTimer


class Feats(ExpCommon):
    def __init__(self, root, name):
        """
        Factory to collecting features from image and frames
        """
        ExpCommon.__init__(self, root, name)
        # create base dir
        ExpCommon.common_path(self, "stores", asure=True)
        self.algo = dict(kp_adap="", kp_core="SIFT",
                         des_adap="", des_core="SIFT")
        self._klass_var()

    def _klass_var(self):
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
            kr = [kp.pt[0], kp.pt[1], kp.size, kp.angle,
                  kp.response, kp.octave, kp.class_id]
            data.append(kr)
        data = None if len(data) is 0 else data
        kdf = pd.DataFrame(data, columns=cols)
        ddf = pd.DataFrame(des)
        # uniform dataframe configs
        kdf[kdf.columns] = kdf[kdf.columns].astype(kdf["x"].dtype)
        ddf.columns = [("d" + str(cc)) for cc in ddf.columns]
        return kdf, ddf

    def __feats_log(self, **opts):
        """
        keys are: key, time, kscnt, kecnt
        kscnt: start keypoint size
        kecnt: end keypoint size
        """
        sinfo = "key: {key}, time: {time}, kps: {kscnt}, kpe: {kecnt}".\
            format(**opts)
        self.elog.info(sinfo)
        self.save_rtlog(opts.keys(), opts.values())

    def __save_feats(self, key, kps, des):
        kdf, ddf = self.__dataframe(kps, des)
        self.save(key+"_kps", kdf)
        self.save(key+"_des", ddf)

    def __featuring(self, feng, deng, imdict):
        """
        Compute and return feature data of one input image
        `feng`: feature detection engine
        `deng`: descriptor detection engine
        `imdict`: image data dictionary
        """
        img = imdict["img"]
        with ExpTimer(verbose=0) as ts:
            kps = feng.detect(img, None)
            kpe, des = deng.compute(img, kps)
        return kps, kpe, des, ts.msecs

    def feats(self, imgs, prefix="f"):
        """
        prefix: `f` represents frame id
        Generate `store/featx/{klass_var}.h5`
            `{prefix}_{:03d}_kps`: keypoints by prefix and id
            `{prefix}_{:03d}_des`: descriptors by prefix and id
            `rtlog`: containing info collected at runtime.
        """
        fd, dd = self.__engine_parts()
        for imd in imgs:
            key = "{}_{:03d}".format(prefix, imd["idx"])
            kps, kpe, des, time = self.__featuring(fd, dd, imd)
            self.__save_feats(key, kpe, des)
            self.__feats_log(key=key, time=time,
                             kscnt=len(kps), kecnt=len(kpe))
        self.elog.info("----- finished-{} -----".format(prefix))

    def clear(self):
        """
        Clear dataset used logs and stores
        """
        self.delete_store()
        self.delete_log()
