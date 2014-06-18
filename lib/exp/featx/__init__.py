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

    def get_feats_pair(self, sid, fid):
        """
        Get features by given `slide`, `frame` pairs
        """
        sk = self.load_feats("s_{:03d}_kps".format(sid))
        sd = self.load_feats("s_{:03d}_des".format(sid))
        fk = self.load_feats("f_{:03d}_kps".format(fid))
        fd = self.load_feats("f_{:03d}_des".format(fid))
        return dict(sk=sk, sd=sd, fk=fk, fd=fd)
