import time


class ExpTimer(object):
    """
    Usage:
        with ht(verbose=True) as t:
            # proc
        print t.msecs, t.tstr()
    """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print("elapsed time: {}".format(self.tstr()))

    def tds(self, ms, fmt):
        d = dict()
        d['dy'], rem = divmod(int(ms), 86400000)
        d["hr"], rem = divmod(rem, 3600000)
        d["mn"], rem = divmod(rem, 60000)
        d["se"], rem = divmod(rem, 1000)
        d['ms'] = int(rem)
        return fmt.format(**d)

    def tstr(self, fmt="{hr:02}:{mn:02}:{se:02}.{ms:03}"):
        return self.tds(self.msecs, fmt)
