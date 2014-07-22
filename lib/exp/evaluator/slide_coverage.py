class SlideCoverage(object):
    def __init__(self, segments):
        self.gseg = segments

    def __get_slide_id(self, fid, tag):
        ret = -1
        fs = tag.fstart
        fe = tag.fstart + tag.duration
        if fs <= fid <= fe:
            ret = tag.sid
        return ret

    def _in_segment(self, fid):
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

    def _mk_xdict(self, fid, ov):
        """
        Get ground truth fid(gfid) and original value(ov)
        """
        sid, dist, gfid = self._in_segment(fid)
        return dict(
            sid=sid, fid=fid, dist=dist, hit_seg_id=gfid, ov=ov)

