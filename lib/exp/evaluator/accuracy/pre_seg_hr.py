from lib.exp.pre import Reducer
from lib.exp.evaluator.ground_truth import GroundTruth
from lib.exp.evaluator.preproc_evaluator import PreprocEvaluator


class PreSegHrBins(object):
    def __init__(self, root, name):
        """
        Preprocessing segmented result hit ratio bins
        """
        self.pp_ = PreprocEvaluator(root, name)
        self.re_ = Reducer(root, name)
        self.gt_ = GroundTruth(root, name)

    def __load_data(self, key, doffset=0):
        rdf = self.re_.load(key)
        rdf.frame_id = rdf.frame_id - doffset
        ddf = self.pp_.ac_segments_df(rdf)
        gsf = self.gt_.load("segments")
        return ddf, gsf

    def __counting(self, pdf, gdf):
        gl = len(gdf)
        # predict not in segment and relly not in segment
        tn = len(pdf[pdf.hit_seg_id < 0].groupby('hit_seg_id'))
        # missed relly not in segment
        fn = (gl - 1) - tn
        # predict in segment and relly in segment
        tp = len(pdf[pdf.hit_seg_id > 0].groupby('hit_seg_id'))
        # missed relly in segment
        fp = gl - tp
        return dict(tn=tn, fn=fn, tp=tp, fp=fp)

    def extract(self, show=True):
        """
        Return extracted bins
        """
        bins = []
        keys = [0,1,2,4,5,6,7]
        for ri, nk, rk, dof in self.re_.zipkey(keys):
            prk = "/nr/{}".format(rk)
            pdf, gdf = self.__load_data(prk, dof)
            binn = self.__counting(pdf, gdf)
            binn.update(key=nk)
            bins.append(binn)
            if show:
                print binn
        return bins
