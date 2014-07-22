__all__ = []

from base import _Base as Base
from core import _Core as Core


class xFrames(Core, Base):
    _xkeys = ["mean", "qart", "top"]

    def __init__(self, pairs=None):
        self.pairs = pairs
        Base.__init__(self, pairs.root, pairs.name)
        Core.__init__(self)

    def crossing(self, pkeys=[]):
        pc = self.pairs
        for keyname, df in pc.iter_data(pkeys, proc=pc.dp_group_fid):
            self._gmm(df, keys=self._xkeys)
            yield keyname, df

    def rev_crossing(self, pkeys=[]):
        """
        Get classified data from pairing class
        pkeys: keys of config set in pair_feats class
        """
        pc = self.pairs
        for keyname, df in pc.iter_data(pkeys, proc=pc.dp_grouping):
            dc = filter(lambda k: k != "fid", df.columns)
            self._gmm(df, keys=dc, post="")
            yield keyname, df
