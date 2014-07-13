__all__ = []

from base import _Base as Base
from core import _Core as Core


class xFrames(Core, Base):
    def __init__(self, root, name, pairs=None):
        if pairs:
            self.pairs = pairs
        Base.__init__(self, root, name)
        Core.__init__(self)

    def crossing(self, pkeys=[]):
        pc = self.pairs
        for kn, df in pc.iter_data(pkeys, proc=pc.dp_group_fid):
            self._gmm(df, keys=["mean", "qart", "top"])
            yield kn, df
