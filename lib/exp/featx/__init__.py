__all__ = []

from lib.exp.tools.slider import Slider
from lib.exp.tools.video import Video
from lib.exp.pre import Reducer
from base import Feats
from preloader import _Preloader as FP
from conf import _Conf as Cfg


class Featx(Feats, Cfg, FP):
    def __init__(self, root, name):
        Feats.__init__(self, root, name)
        Cfg.__init__(self)

    def slide_feats(self):
        # compute feats of slides
        ss = Slider(self.root, self.name)
        imgl = ss.get_slides(None, gray=True, resize=True)
        self.feats(imgl, prefix="s")

    def frame_feats(self):
        # Compute feats of frames
        rr = Reducer(self.root, self.name)
        vv = Video(self.root, self.name)
        imgl = vv.get_frames(rr.frame_ids(ikey=4), gray=True)
        self.feats(imgl, prefix="f")

    def get_feats_pair(self, sid, fid):
        """
        Deprecated, use `feats_pair` instead
        Get features by given `slide`, `frame` pairs
        """
        sk = self.load_feats("s_{:03d}_kps".format(sid))
        sd = self.load_feats("s_{:03d}_des".format(sid))
        fk = self.load_feats("f_{:03d}_kps".format(fid))
        fd = self.load_feats("f_{:03d}_des".format(fid))
        return dict(sk=sk, sd=sd, fk=fk, fd=fd)

    def feats_pair(self, isx, ifx):
        """
        Get (pid, kps, des) data
        """
        self.preload_packs(True)
        return dict(slide=self.slides[isx],
                    frame=self.frames[ifx])
