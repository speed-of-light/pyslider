__doc__ = """
Pairing features extraced from `featx`
"""

__all__ = []

from base import _Base as Pbase


class PairFeats(Pbase):
    def __init__(self, fx=None):
        self.featx = fx
        Pbase.__init__(self, self.featx.root, self.featx.name)

    def __batch_job(func):
        def inner(self, *args, **kwargs):
            keys = kwargs["keys"]
            if len(keys) == 0:
                keys = range(len(self._epre))
            for vd in self._epre[keys]:
                self.set_dict_vars(vd["ev"])
                Pbase._reload(self, "pcore")
                func(self, *args, **kwargs)
        return inner

    @__batch_job
    def exp_ss_mat(self, keys=[]):
        # Making slide feats confusion matrix
        self._batch_slides_pairing()

    @__batch_job
    def exp(self, keys=[], rngs=123):
        self._batch_pairing()  # fs=rngs, fe=rngs+3)
