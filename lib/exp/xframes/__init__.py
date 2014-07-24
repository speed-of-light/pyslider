__all__ = []

from base import _Base as Base
from core import _Core as Core
from slide_voter import SlideVoter as SV


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

    def slides_ans(self, key, voters=[], name=""):
        cdf = self.rev_crossing(pkeys=[key]).next()[1]
        pdf = self.pairs.iter_data([key], proc=None).next()[1]
        ssf = self.pairs.load(self.pairs._keyset([key])[0][1])
        sv = SV(self.root, self.name, ssf)
        return sv.votes(cdf, pdf, voters, name=name)
