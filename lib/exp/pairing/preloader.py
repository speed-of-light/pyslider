import cv2
from lib.exp.featx import Featx


class _Preloader(object):
    def __init__(self):
        """
        Preloading handlers
        Grabing data
        """
        pass
        # self.__preload("featx")

    def __load_mod(self, mod):
        if mod == "matcher":
            _mod = cv2.DescriptorMatcher_create(self.mcore)
        elif mod == "featx":
            _mod = Featx(self.root, self.name)
        self.__dict__[mod] = _mod

    def _reload_mod(self, mod):
        self.__load_mod(mod)

    def preload(self, mod):
        if not hasattr(self, mod):
            self._reload_mod(mod)

    def get_mod(self, mod):
        self._preload(mod)
        return self.__dict__[mod]
