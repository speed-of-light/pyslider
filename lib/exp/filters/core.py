class FilterBase(object):
    """
    Interface of filter classes
    """
    def __init__(self, matchx):
        """
        data: dict includes keys:
            `matches`,
            `slide feats`,
            `video frame feats`,
            `slide size(qsize)`
        """
        self.matchx = matchx

    def pair_data(self, sid, fid, df):
        """
        Return common need data pointers
        """
        good = df
        skps, fkps = self.matchx.fx.load_keypoints_pair(sid, fid)
        return dict(good=good, skps=skps, fkps=fkps)
