__doc__ = """
Pairing features extraced from `featx`
"""

__all__ = []

from base import _Base as Pbase


class PairFeats(Pbase):
    _e_NND = [dict(en="BBF .7", ev=.7001),
              dict(en="BBF .8", ev=.8001),
              dict(en="BBF .9", ev=.9001),
              dict(en="BBF 1.", ev=1.0001) ]

    def __init__(self, root, name, fx=None):
        if fx:
            self.featx = fx
        Pbase.__init__(self, root, name)

    def confusion_slide_feats(self):
        # Making slide feats confusion matrix
        pass

    def exp_nn_dist(self):
        for nnd in self._e_NND:
            self.set_var("nn_dist", nnd["ev"], log=True)
            self._batch_pairing(24, 25)
