__all__ = []

from lib.exp.featx.base import Featx
from lib.exp.tools.slider import Slider


class SlideFeatx(Featx, Slider):
    def __init__(self, root, name):
        Featx.__init__(self, root, name)
        Slider.__init__(self, root, name)

    def get_feats(self):
        imgl = self.get_slides(None, gray=True, resize=True)
        self.feats(imgl, prefix="s")
