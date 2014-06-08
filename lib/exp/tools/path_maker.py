import os
from tools import ToolHelper as TH


class PathMaker(object):
    def __init__(self, root, name):
        self.root = root
        self.name = name

    def make(self, resource='stores', ext='h5', asure=True, root=False):
        """
        resource: resource name in path
        ext: file extension for resource, if None then return only path
        asure: make sure the path exist
        root: get only root path of given resource
        usage:
            # make simple log path, and make sure created
            self.make_path('log', None)
            # make path for log with log extension, and not check existence
            self.make_path('log', 'log', False)
        """
        rp = self.__root(resource)
        if root:
            return rp
        if asure:
            self._asure_path(rp)
        cn = TH._underscore(self.__class__.__name__)
        rp = "{}/{}".format(rp, cn)
        if ext is not None:
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
