from lib.exp.base import ExpCommon
from preloader import _Preloader


class _Base(ExpCommon):
    def __init__(self, root, name):
        """
        Configurations
        Common processing
        Core paring
        """
        ExpCommon.__init__(self, root, name)
        ExpCommon.common_path(self, "stores", asure=True)
