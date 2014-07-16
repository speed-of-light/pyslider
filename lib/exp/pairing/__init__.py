__doc__ = """
Pairing features extraced from `featx`
"""

__all__ = []

from base import _Base as Pbase


class PairFeats(Pbase):
    def __init__(self, fx=None):
        self.featx = fx
        Pbase.__init__(self, self.featx.root, self.featx.name)

    def exp_ss_mat(self):
        # Making slide feats confusion matrix
        self._batch_slides_pairing()

    def exp_nn_dist(self, keys=[]):
        if len(keys) == 0:
            keys = range(len(self._epre))
        for vd in self._epre[keys]:
            self.set_dict_vars(vd)
            self._batch_pairing()
