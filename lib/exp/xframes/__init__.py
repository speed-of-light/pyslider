__all__ = []

from base import _Base as Base


class xFrames(Base):
    def __init__(self, root, name, pairs=None):
        Base.__init__(self, root, name, pairs)

    def cross_no_slides(self):
        pass
