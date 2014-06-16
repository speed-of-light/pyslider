__all__ = ["batcher", "doer"]

from match_do import MatchDo
from mark_do import MarkDo


class Doer(MatchDo, MarkDo):
    def __init__(self, root, name):
        """
        A class doing procedural things
        """
        MarkDo.__init__(self, root, name)
        pass
