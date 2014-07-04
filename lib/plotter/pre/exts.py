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

    def _get_reduced_data(self, re, rk, pp):
        prk = "/reduce/{}".format(rk)
        red = re.load(prk)
        scf = pp.ac_reduced_to_slides(red)
        return scf
