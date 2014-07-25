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

    VOTES = [
        dict(voters=["area"], name="v_a"),
        dict(name="v_at", voters=["area", "top50"]),
        dict(name="v_atm", voters=["area", "top50", "mean"]),
        dict(name="v_atmr",
             voters=["area", "top50", "mean", "rmean"]),
        dict(name="v_atmri",
             voters=["area", "top50", "mean", "rmean", "invr"]),
        dict(name="v_at_64", voters=["area", "top50"],
             wts=[.6, .4]),
        dict(name="v_at_73", voters=["area", "top50"],
             wts=[.7, .3]),
        dict(name="v_atm_721", voters=["area", "top50", "mean"],
             wts=[.7, .2, .1]),
        dict(name="v_atm_253", voters=["area", "top50", "mean"],
             wts=[.2, .5, .3]),
        dict(name="v_atm_533", voters=["area", "top50", "mean"],
             wts=[.5, .3, .2]),
        dict(name="v_atm_433", voters=["area", "top50", "mean"],
             wts=[.4, .3, .3]),
        dict(name="v_atm_442", voters=["area", "top50", "mean"],
             wts=[.2, .4, .4]),
        dict(name="v_atm_re", voters=["area", "top50", "mean"],
             wts="even refine"),
        ]

    def slides_ans(self, key):
        cdf = self.rev_crossing(pkeys=[key]).next()[1]
        pdf = self.pairs.iter_data([key], proc=None).next()[1]
        ssf = self.pairs.load(self.pairs._keyset([key])[0][1])
        sv = SV(self.root, self.name, cdf, pdf, ssf)
        for vt in self.VOTES:
            sv.votes(**vt)
        return sv.vdf
