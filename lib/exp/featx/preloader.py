from lib.exp.summary import Summary
from lib.exp.pre import Reducer


class _Preloader(object):
    def __init__(self):
        pass

    def __slide_seeds(self):
        su = Summary()
        sids = range(1, su.info(self.root, self.name).n_slides+1)
        return sids

    def __frame_seeds(self, key=4):
        # key = index of "/nr/diff_next/size_30"
        rr = Reducer(self.root, self.name)
        fids = rr.frame_ids(ikey=key)
        return fids

    def __sf_seeds(self, key=4):
        # key = index of "/nr/diff_next/size_30"
        sids = self.__slide_seeds()
        fids = self.__frame_seeds(key)
        return sids, fids

    def _seeds(self, key):
        if key == "slide":
            pids = self.__slide_seeds()
        elif key == "frame":
            pids = self.__frame_seeds()
        return pids

    def __base_loader(self, key):
        fd = self.load(key)
        if fd is None:
            return []
        return fd

    def __load_feats_fac(self, pf, pk):
        fx = lambda pid: self.__load_feats(pf=pf, pk=key, pid=pid)
        return fx

    def __load_feats(self, pf="slide", pid=1, key="des"):
        pk = "{}_{:03d}_{}".format(pf[0], pid, key)
        return self.__base_loader(pk)

    def __load_feats_list(self, pids=[], pf="frame", key="des"):
        fs = []
        self.elog.info("loading {} feats ({})...".format(pf, key))
        fs = map(self.__load_feats_fac(pf, key), pids)
        self.elog.info("Load {} feats ({}) finished...".format(pf, key))
        return fs

    def reload(self, key="slide_des"):
        pf, pkey = key.split("_")
        pids = self._seeds(pf)
        data = self.__load_feats(pids, pf, pkey)
        self.__dict__[key] = data

    def preload(self, key="slide_des"):
        """`slide_kps`, `slide_des`, `frame_kps`, `frame_des`"""
        if not hasattr(self, key):
            self.__reload(key)
