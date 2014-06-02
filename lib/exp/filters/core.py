class KpFilter(object):
    """
    Interface of filter classes
    """
    def __init__(self, data):
        """
        data: dict includes keys: `matches`, `slide feats`, `video frame feats`,
            `slide size(qsize)`
        """
        self.data = data

    def filter(self):
        print "Should implement methods to compute and filter matched result"
