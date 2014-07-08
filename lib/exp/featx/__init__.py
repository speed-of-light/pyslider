__all__ = []

from lib.exp.tools.slider import Slider
from lib.exp.tools.video import Video
from lib.exp.pre import Reducer
from base import Feats


class Featx(Feats):
    def __init__(self, root, name):
        Feats.__init__(self, root, name)

    def confusion_slide_feats(self):
        # Making slide feats confusion matrix
        pass

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

    def load_slides_feats(self, sids):
        sfs = []
        for sid in sids:
            sfs.append(self.load_feats("s_{:03d}_des".format(sid)))
        self.elog.info("loading {}-{} slides feats ...".
                       format(self.root, self.name))
        return sfs

    def load_frame_feats(self, fid):
        return self.load_feats("f_{:03d}_des".format(fid))
