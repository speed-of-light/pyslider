from lib.exp.pre import Reducer
from preproc_evaluator import PreprocEvaluator
from lib.exp.evaluator.ground_truth import GroundTruth


class PreSegHrBins(object):
    def __init__(self, root, name):
        """
        Preprocessing segmented result hit ratio bins
        """
        self.__load_const()
        self.pp_ = PreprocEvaluator(root, name)
        self.re_ = Reducer(root, name)
        self.gt_ = GroundTruth(root, name)

    def __load_const(self):
        methods = ["Avg 2", "Avg 10", "Avg 15", "Avg 20",
                   "Avg 30", "Avg 60", "Avg 300", "Bkg Model"]
        rkeys = ["diff_next/size_2", "dn/size_10",
                 "diff_next/size_15", "dn/size_20",
                 "diff_next/size_30", "diff_next/size_60",
                 "diff_next/size_300", "diff_bkg"]
        self.funs = methods
        self.keys = rkeys

    def __load_data(self, key):
        df = self.re_.load(key)
        ddf = self.pp_.ac_segments_df(df)
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
        for rk in self.keys:
            prk = "/nr/{}".format(rk)
            pdf, gdf = self.__load_data(prk)
            binn = self.__counting(pdf, gdf)
            binn.update(key=rk)
            bins.append(binn)
            if show:
                print binn
        return bins
