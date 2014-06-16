__all__ = []

from lib.exp.featx.base import Feats
from lib.exp.tools.slider import Slider
from lib.exp.tools.video import Video
from lib.exp.prepare import Prepare


class Featx(Feats):
    def __init__(self, root, name):
        Feats.__init__(self, root, name)

    def get_slide_feats(self):
        ss = Slider(self.root, self.name)
        imgl = ss.get_slides(None, gray=True, resize=True)
        self.feats(imgl, prefix="s")

    def get_frame_feats(self):
        pp = Prepare(self.root, self.name)
        vv = Video(self.root, self.name)
        imgl = vv.get_frames(pp.frame_ids(), gray=True)
        self.feats(imgl, prefix="f")
