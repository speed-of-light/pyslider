class Predictor(object):
    def __init__(self, fids, matches):
        """
        matches: dataframe contains `dist`, `slide keypoint`, `frame keypoint`
        """
        self.fids = fids
        self.matches = matches
