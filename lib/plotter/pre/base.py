

class _Base(object):
    def __init__(self):
        pass

    def __key_is_blank(self, key):
        sd = self.__dict__
        return (not hasattr(self, key)) or (sd[key] is None) or (sd[key] == "")

    def __rootname_not_set(self):
        return self.__key_is_blank("root") or \
            self.__key_is_blank("name")

    def _assert_rootname_exist(self):
        if self.__rootname_not_set():
            info = "set_rootname() before calling this function"
            print info
            raise Exception("Error", info)

    def set_rootname(self, root, name):
        self.root = root
        self.name = name
        self.rn = "{}_{}".format(root, name)
        self.rootname = "[Data: {}-{}]".format(root, name)

    def _title_tag(self, info):
        title = "{} {}".format(self.rootname, info)
        return title

    def _common_axes(self, fig):
        ax = fig.add_subplot(111)
        ax.patch.set_alpha(.0)
        return ax
