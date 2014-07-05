import pandas as pd
from lib.exp.summary import Summary
from lib.exp.evaluator.preproc_evaluator import PreprocEvaluator
from lib.exp.pre import Reducer
from lib.exp.evaluator.accuracy import Accuracy


class _Exts(object):
    def __init__(self):
        pass

    def __slide_count(self):
        self._reload_obj("summary")
        return self.su_.info(self.root, self.name).n_slides

    def _reload_obj(self, obj_name):
        if obj_name == "reducer":
            self.re_ = Reducer(self.root, self.name)
        elif obj_name == "preproc":
            self.pp_ = PreprocEvaluator(self.root, self.name)
        elif obj_name == "summary":
            self.su_ = Summary()

    def _get_reduced_data(self, re, rk, pp):
        prk = "/nr/{}".format(rk)
        red = re.load(prk)
        scf = pp.ac_reduced_to_slides(red)
        return scf

    def _get_slide_coverages(self, keyzip):
        """
        Load slide coverage and slide hitratio data
        """
        self._reload_obj("reducer")
        self._reload_obj("preproc")
        pda = []
        for ri, na, rk in keyzip:
            prk = "/nr/{}".format(rk)
            red = self.re_.load(prk)
            sc, sh = self.pp_.preview(red, self.__slide_count())
            pda.append(
                dict(method=na, slide_coverage=sc, segments_hit_ratio=sh))
        return pd.DataFrame(pda)

    def _get_accuracy(self, root, name):
        aa = Accuracy()
        aa.set_data(root, name, aa.PreprocessSegmentHitRatio)
        req = ["accuracy", "precision", "sensitivity"]
        return aa.details(req, show=0)
