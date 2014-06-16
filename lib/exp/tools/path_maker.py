import os
from lib import Dataset
from lib.exp.tools import ToolHelper as TH


class PathMaker(Dataset):
    def __init__(self, root, name):
        Dataset.__init__(self, root, name)

    def common_path(self, resource="stores", kvar="", ext="h5", asure=True):
        """
        res: resource name in path
        kvar: klass variables
        ext: file extension for resource, if None then return only path
        asure: make sure the path exist
        usage:
            # make simple log path, and make sure created
            self.common_path('log', None)
            # make path for log with log extension, and not check existence
            self.common_path('log', 'log', False)
        """
        rp = self.__root(resource)
        cn = TH.underscore(self.__class__.__name__)
        rp = "{}/{}".format(rp, cn)
        if kvar:
            rp = "{}/{}".format(rp, kvar)
        if asure:
            self.__asure_path(rp)
        if ext:
            rp = "{}.{}".format(rp, ext)
        return rp

    def __asure_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __root(self, resource):
        rt = self.root
        pn = self.name
        pth = "data/{}/{}/{}".format(rt, pn, resource)
        return pth

    def __rm_file_path(self, fp):
        if os.path.isfile(fp):
            print "{} removed".format(fp)
            os.remove(fp)
