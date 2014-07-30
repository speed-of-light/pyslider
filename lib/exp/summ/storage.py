import os
from lib.exp.tools.slider import Slider
from lib.exp.tools.video import Video
from lib.exp.pre import Reducer
from lib.exp.featx import Featx
from lib.exp.match import Matchx
from lib.exp.pairing import PairFeats
from lib.exp.xframes import xFrames
from lib.exp.evaluator.xframes import XframeEval


class _Storage(object):
    sna = ["dsn", "Slides", "Video", "Preprocess", "Features", "Matches",
           "Classifier", "Recognizer"]

    def __init__(self, r, n):
        pv = self.__load_allsize(r, n)
        pa = map(lambda v: v >> 20, pv)
        self.sd = dict(zip(self.sna, [n] + pa))

    def __load_allsize(self, r, n):
        ps = []
        ps.append(self._sps(Slider(r, n).pdf_path[:-4]))
        ps.append(self._sps(Video(r, n).stream_path))
        ps.append(Reducer(r, n)._store_size())
        fx = Featx(r, n)
        ps.append( fx._store_size() )
        pf = Matchx(r, n)
        ps.append( pf._store_size() )
        xf = xFrames(pf)
        ps.append( xf._store_size() )
        xfe = XframeEval(xf)
        ps.append( xfe._store_size() )
        return ps

    def _sps(self, sp):
        return os.path.getsize(sp)
