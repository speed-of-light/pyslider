from lib.exp.base import ExpCommon
from ground_truth import GroundTruth


class PreprocEvaluator(ExpCommon):
    def __init__(self, root, name):
        """
        Evaluate preprocess effectiveness
        Depends on `GroundTruth` should include `segments` dataframe
        """
        ExpCommon.__init__(self, root, name)
        self.__load_segments_gnd()

    def __load_segments_gnd(self):
        gt = GroundTruth(self.root, self.name)
        self.seg = gt.load("segments")

    def __get_slide_id(self, fid, tag):
        ret = -1
        fs = tag.fstart
        fe = tag.fstart + tag.duration
        if fs <= fid <= fe:
            ret = tag.sid
        return ret

    def in_segment(self, fid):
        """
        Return value if frame is in the segments
        """
        dfi = self.seg[self.seg.fstart <= fid]
        dist = None
        sid = -1
        if len(dfi) > 0:
            tag = dfi.iloc[-1]
            sid = self.__get_slide_id(fid, tag)
            if sid > 0:
                dist = fid - tag.fstart
        return sid, dist
