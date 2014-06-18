import cv2


class Preloader(object):
    def __reload_slide_feats(self):
        sids = self.slide_seeds()
        self.sfx = self.fx.load_slides_feats(sids)

    def __preload_slide_feats(self):
        if not hasattr(self, "sfx"):
            self.__reload_slide_feats()

    def __preload_matcher(self):
        if not hasattr(self, "matcher"):
            self._reload_matcher()

    def _load_matcher(self):
        return cv2.DescriptorMatcher_create(self.mcore)

    def _reload_matcher(self):
        self.matcher = self._load_matcher()

    def _preload(self):
        self.__preload_slide_feats()
        self.__preload_matcher()

    def get_matcher(self):
        if not hasattr(self, "matcher"):
            return self._load_matcher()
        else:
            return self.matcher
