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
        self.gseg = gt.load("segments")

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
        dfi = self.gseg[self.gseg.fstart <= fid]
        dist = None
        sid = -1
        gnd_fid = None
        if len(dfi) > 0:
            tag = dfi.iloc[-1]
            sid = self.__get_slide_id(fid, tag)
            gnd_fid = tag.fstart * -1
            if sid > 0:
                gnd_fid = tag.fstart
                dist = fid - tag.fstart
        return sid, dist, gnd_fid

    def ac_segments_df(self, reduced):
        data = []
        for ri, rd in reduced.iterrows():
            fid = rd.frame_id
            sid, dist, gfid = self.in_segment(fid)
            data.append(
                dict(sid=sid, fid=fid, dist=dist, hit_seg_id=gfid,
                     diff=rd['diff']))
        return pd.DataFrame(data)

    def ac_slide_count(self, segments):
        slide_seg = segments[segments.dist.notnull()]
        smi = []
        for dgi, dg in slide_seg.groupby("sid"):
            smi.append(dg.dist.argmin())
        return segments.iloc[smi]

    def ac_reduced_to_slides(self, reduced):
        seg = self.ac_segments_df(reduced)
        sdf = self.ac_slide_count(seg)
        return sdf

    def slide_coverage(self, reduced, total_slides):
        sdf = self.ac_reduced_to_slides(reduced)
        return len(sdf)*1.0/total_slides

    def segment_hit_count(self, reduced):
        seg = self.ac_segments_df(reduced)
        seg = seg[seg.hit_seg_id.notnull() & (seg.hit_seg_id > 0)]
        hsi = []
        for gsi, gs in seg.groupby("hit_seg_id"):
            hsi.append(gs.hit_seg_id)
        return len(hsi)

    def preview(self, reduced, total_slides):
        scc = len(self.ac_reduced_to_slides(reduced))
        shc = self.segment_hit_count(reduced)
        gsc = len(self.gseg)
        pd = dict(
            total_slides=total_slides,
            gnd_segments=gsc,
            slide_count=scc,
            segment_hits=shc,
            slide_coverage=scc*1./total_slides,
            segments_hit_ratio=shc*1./gsc)
        return pd
