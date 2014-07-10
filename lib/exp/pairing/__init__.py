__doc__ = """
Pairing features extraced from `featx`
"""

__all__ = []

from base import _Base as Pbase


class PairFeats(Pbase):
    def __init__(self, root, name):
        Pbase.__init__(self, root, name)

    def confusion_slide_feats(self):
        # Making slide feats confusion matrix
        pass

    def pairing(self, fs=0, fe=-1, save=False):
        self._update_klass_var()
        sdl = []
        for fx in self.featx.frames[fs:fe]:
            for sx in self.featx.slides:
                pin = "Pairing s-{: 3d}, f-{: 5d}"
                self.elog.info(pin.format(sx["pid"], fx["pid"]))
                dp = dict(frame=fx, slide=sx)
                sdl.append(self._pairing(dp, nn_dist=0.9, save=save))
        self._save_rtlog(sdl)
        return sdl
