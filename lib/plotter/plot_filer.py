import os
import re
import inspect


class _PlotFiler(object):
    def __init__(self):
        """
        Provide common functions to save plots
        """
        self.autosave_fig = False

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
        base = "data/fig/{ft}/{ctype}/{method}"
        root = base.format(**args)
        self.__asure_path(root)
        return "{}/{}.svg".format(root, name)

    def __underscore(self, string=""):
        first_cap_re = re.compile("(.)([A-Z][a-z]+)")
        all_cap_re = re.compile("([a-z0-9])([A-Z])")
        s1 = first_cap_re.sub(r"\1_\2", string)
        return all_cap_re.sub(r"\1_\2", s1).lower()

    def _savefig(self, figh, func, name):
        if not self.autosave_fig:
            return
        fp = self.__make_path(ft="svg", method=func, name=name)
        figh.savefig(fg, frame_on=0)
        print "Figure saved to {}".format(fp)
