__doc__ = """
Auto latexer for experimental results.
"""
__all__ = []

from nsf_roc_tab import NsfRocTab


class Texer(object):
    def __init__(self):
        pass

    def no_sf_roc(self, data):
        nrt = NsfRocTab()
        return nrt.tabular(data)
