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

    def filter_(self):
        """
        Return common need data pointers
        """
        good = self.data['matches']
        skp = self.data['sif']['kps']
        fkp = self.data['vif']['kps']
        return good, skp, fkp
