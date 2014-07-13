from video import Video


class Preloader(object):
    def __init__(self):
        """
        A helper to reload modules
        """
        pass

    def _reload(self, module="video"):
        if module == "video":
            mod = Video(self.root, self.name)
        self.__dict__[module] = mod

    def _preload(self, module="video"):
        if not hasattr(self, module):
            print "preload {}".format(module)
            self._reload(module)

    def __mod_not_load(self, module="video"):
        return (not hasattr(self, module)) or \
            (self.__dict__[module] is None)

    def _assert_loaded(self, module="video"):
        if self.__mod_not_load(module):
            info = "Module {} not loaded".format(module)
            raise Exception("Error", info)

    def __invalid_str_attr(self, name):
        return (not hasattr(self, name)) or \
            (self.__dict__[name] is None) or (self.__dict__[name] == "")

    def _assert_valid_str(self, name):
        if self.__invalid_str_attr(name):
            info = "Attribute {} is invalid.".format(name)
            raise Exception("Invalid Attribute Error", info)
