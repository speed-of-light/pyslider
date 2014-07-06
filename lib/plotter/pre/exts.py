import pandas as pd
from lib.exp.summary import Summary
from lib.exp.evaluator.preproc_evaluator import PreprocEvaluator
from lib.exp.pre import Const
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

    def __find_dof(self, key):
        di = Const.Doffsets[Const.Rkeys.index(key)]
        return di

    def _get_reduced_data(self, rk, dof):
        self._reload_obj("reducer")
        prk = "/nr/{}".format(rk)
        rdf = self.re_.load(prk)
        rdf.frame_id = rdf.frame_id - dof
        return rdf

    def _get_reduced_slides(self, rk, doffset=0):
        rdf = self._get_reduced_data(rk, doffset)
        self._reload_obj("preproc")
        sdf = self.pp_.ac_reduced_to_slides(rdf)
        return sdf

    def _get_reduced_segments(self, rk):
        dof = self.__find_dof(rk)
        rdf = self._get_reduced_data(rk, dof)
        self._reload_obj("preproc")
        sdf = self.pp_.ac_segments_df(rdf)
        return sdf

    def _get_slide_coverages(self, keyzip):
        """
        Load slide coverage and slide hitratio data
        """
        self._reload_obj("reducer")
        self._reload_obj("preproc")
        pda = []
        for ri, na, rk, dof in keyzip:
            prk = "/nr/{}".format(rk)
            red = self.re_.load(prk)
            red.frame_id = red.frame_id - dof
            pdc = self.pp_.preview(red, self.__slide_count())
            pdc.update(method=na)
            pda.append(pdc)
        return pd.DataFrame(pda)

    def _get_accuracy(self):
        aa = Accuracy()
        aa.set_data(self.root, self.name, aa.PreprocessSegmentHitRatio)
        req = ["accuracy", "precision", "sensitivity"]
        return aa.details(req, show=0)
