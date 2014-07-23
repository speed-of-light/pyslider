__doc__ = """
Auto latexer for experimental results.
"""
__all__ = []

from nsf_roc_tab import NsfRocTab
from nsf_cov_tab import NsfCovTab


class Texer(object):
    def __init__(self):
        pass

    def nsf_roc(self, data):
        tab = NsfRocTab()
        return tab.tabular(data)

    def nsf_cov(self, data, sels=[0, 1, 5, 6, 7]):
        tab = NsfCovTab()
        return tab.tabular(sels, data)
