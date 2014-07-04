import pandas as pd
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
        tagid = None
        if len(dfi) > 0:
            tag = dfi.iloc[-1]
            sid = self.__get_slide_id(fid, tag)
            if sid > 0:
                tagid = tag.fstart
                dist = fid - tag.fstart
        return sid, dist, tagid

    def ac_segments_df(self, reduced):
        data = []
        for ri, rd in reduced.iterrows():
            sid, dist, hid = self.in_segment(rd.frame_id)
            data.append(
                dict(sid=sid, fid=rd.name, dist=dist,
                     hit_seg_id=hid, diff=rd['diff']))
        return pd.DataFrame(data)

    def ac_slide_count(self, segments):
        slide_seg = segments[segments.dist.notnull()]
        smi = []
        for dgi, dg in slide_seg.groupby("sid"):
            smi.append(dg.dist.argmin())
        return segments.iloc[smi]

    def slide_coverage(self, reduced, total_slides):
        seg = self.ac_segments_df(reduced)
        sdf = self.ac_slide_count(seg)
        return len(sdf)*1.0/total_slides

    def segment_hit_ratio(self, reduced):
        seg = self.ac_segments_df(reduced)
        seg = seg[seg.hit_seg_id.notnull()]
        hsi = []
        for gsi, gs in seg.groupby("hit_seg_id"):
            hsi.append(gs.hit_seg_id)
        return len(hsi)*1.0/len(self.seg)

    def preview(self, reduced, total_slides):
        sc = self.slide_coverage(reduced, total_slides)
        shr = self.segment_hit_ratio(reduced)
        print "Slide coverage: {:5.3f},".format(sc) + \
            "Segment hit ratio: {:5.3f}".format(shr)
        return sc, shr
