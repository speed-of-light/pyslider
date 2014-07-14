import os
import re
import inspect


class _PlotFiler(object):
    def __init__(self):
        """
        Provide common functions to save plots
        """
        self.save_fig = False

    def __assert_name_exist(self, name):
        if (name is None) or (name == ""):
            info = "File name is not set"
            raise Exception("Error", info)

    def __classname(self):
        scn = self.__class__.__name__
        pi = scn.index("Plotter")
        uscn = self.__underscore(scn[:pi])
        return uscn

    def __asure_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __make_path(self, ft="svg", method="error", name=None):
        self.__assert_name_exist(name)
        ctype = self.__classname()
        args = dict(ft=ft, ctype=ctype, method=method)
        base = "data/fig/{ctype}/{method}"
        root = base.format(**args)
        self.__asure_path(root)
        return "{}/{}.{}".format(root, name, ft)

    def __underscore(self, string=""):
        first_cap_re = re.compile("(.)([A-Z][a-z]+)")
        all_cap_re = re.compile("([a-z0-9])([A-Z])")
        s1 = first_cap_re.sub(r"\1_\2", string)
        return all_cap_re.sub(r"\1_\2", s1).lower()

    def _savefig(self, figh, func, name):
        if not self.save_fig:
            return
        fp = self.__make_path(ft="eps", method=func, name=name)
        figh.savefig(fp, transparent=1)
        print "Figure saved to {}".format(fp)
