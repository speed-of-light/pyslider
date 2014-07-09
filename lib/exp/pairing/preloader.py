from lib.exp.featx import Featx


class _Preloader(object):
    def __init__(self):
        """
        Preloading handlers
        Grabing data
        """
        pass

    def __preload_matcher(self):
        if not hasattr(self, "matcher"):
            self._reload_matcher()

    def _load_matcher(self):
        self.matcher = cv2.DescriptorMatcher_create(self.mcore)

    def _reload_matcher(self):
        self.matcher = self._load_matcher()

    def _preload(self):
        self.__preload_matcher()

    def get_matcher(self):
        if not hasattr(self, "matcher"):
            return self._load_matcher()
        else:
            return self.matcher
