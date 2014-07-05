import pandas as pd
from lib.exp.summary import Summary
from lib.exp.evaluator.preproc_evaluator import PreprocEvaluator
from lib.exp.pre import Reducer


class _Exts(object):
    def __init__(self):
        pass

    def _reload_obj(self, root, name, obj_name):
        if obj_name == "reducer":
            self.re_ = Reducer(root, name)
        elif obj_name == "preproc":
            self.pp_ = PreprocEvaluator(root, name)
        elif obj_name == "summary":
            self.su_ = Summary()

    def _get_reduced_data(self, re, rk, pp):
        prk = "/nr/{}".format(rk)
        red = re.load(prk)
        scf = pp.ac_reduced_to_slides(red)
        return scf

    def __slide_count(self, root, name):
        self._reload_obj(root, name, "summary")
        return self.su_.info(root, name).n_slides

    def _get_slide_coverages(self, root, name, keyzip):
        """
        Load slide coverage and slide hitratio data
        """
        self._reload_obj(root, name, "reducer")
        self._reload_obj(root, name, "preproc")
        pda = []
        for ri, na, rk in keyzip:
            prk = "/nr/{}".format(rk)
            red = self.re_.load(prk)
            sc, sh = self.pp_.preview(red, self.__slide_count(root, name))
            pda.append(
                dict(method=na, slide_coverage=sc, segments_hit_ratio=sh))
        return pd.DataFrame(pda)
