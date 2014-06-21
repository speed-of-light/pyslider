__all__ = []

from lib.exp.featx.base import Feats
from lib.exp.tools.slider import Slider
from lib.exp.tools.video import Video
from lib.exp.pre import Reducer


class Featx(Feats):
    def __init__(self, root, name):
        Feats.__init__(self, root, name)

    def get_slide_feats(self):
        ss = Slider(self.root, self.name)
        imgl = ss.get_slides(None, gray=True, resize=True)
        self.feats(imgl, prefix="s")

    def get_frame_feats(self):
        rr = Reducer(self.root, self.name)
        vv = Video(self.root, self.name)
        imgl = vv.get_frames(rr.frame_ids(), gray=True)
        self.feats(imgl, prefix="f")

    def load_feats(self, key):
        fd = self.load(key)
        if fd is None:
            return []
        return fd

    def get_feats_pair(self, sid, fid, keys=["kps"]):
        """
        Get features by given `slide`, `frame` pairs
        keys: ["kps", "des"] or both
        """
        dd = dict(sid=sid, fid=fid)
        for key in keys:
            dd["s"+key[0]] = self.load_feats("s_{:03d}_{}".format(sid, key))
            dd["f"+key[0]] = self.load_feats("f_{:03d}_{}".format(fid, key))
        return dd

    def load_keypoints_pair(self, sid, fid):
        data = self.get_feats_pair(sid, fid)
        skps = self._to_keypoints(data["sk"])
        fkps = self._to_keypoints(data["fk"])
        return skps, fkps

    def load_slides_feats(self, sids):
        sfs = []
        for sid in sids:
            sfs.append(self.load_feats("s_{:03d}_des".format(sid)))
        self.elog.info("loading {}-{} slides feats ...".
                       format(self.root, self.name))
        return sfs

    def load_frame_feats(self, fid):
        return self.load_feats("f_{:03d}_des".format(fid))
