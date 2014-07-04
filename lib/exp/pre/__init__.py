__doc__ = """
Preprocess input data, include
    `video` format should be `avi` or `mp4`
    `slide` format should be `pdf` and auto-convert to `jpg` or
        a set of `jpg` images
    `summary` save `video` and `slide` infomation to summary store
    `reducer` reduce video frames to more distingushable one
    `reducer.probe` probing video to compute distingushable posibility position
"""

__all__ = []

import numpy as np
from lib.exp.base import ExpCommon


class Reducer(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)

    def __compress(self, data, keep_last=False):
        """
        Get the compressed dataset and compressed ratio
        """
        before = len(data)
        maxv = data.iloc[0].name
        prev = data.iloc[0].name
        for curv in data.index[1:]:
            if (curv - prev) == 1:  # continuous sequence
                if data.ix[maxv]['diff'] < data.ix[curv]['diff']:
                    # drop previous max if its diff smaller
                    data = data.drop([maxv])
                    maxv = curv
                else:  # drop continuous item
                    data = data.drop([curv])
            else:  # seperate sequence start
                maxv = curv
            prev = curv
        return data, before, len(data)

    def __get_data(self, key):
        """
        Get probed `differenc` values and `frame` data
        """
        df = self.load(key)
        dmean = df["diff"].mean()
        can = df[df["diff"].gt(dmean)]
        return can, len(df)

    def __results(self, **opts):
        oo = opts["origin"]
        ff = opts["final"]
        info = "Original: {}, thresed: {}, final: {}, ratio: {}".\
            format(oo, opts["thresed"], ff, ff*1.0/oo)
        istr = "Reduce data from {}".format(info)
        print istr
        self.elog.info(istr)
        self.save_rtlog(opts.keys(), opts.values())

    def reduce(self, key):
        can, orl = self.__get_data(key)
        red, thresed, after = self.__compress(can)
        self.__results(key=key, origin=orl,
                       thresed=thresed, final=after)
        return red

    def clear(self):
        self.delete_log()
        # self.delete_store()  # be careful

    def frame_ids(self, key="/reduce/diff_next/size_30"):
        df = self.load(key)
        return df.frame_id.values.astype(np.int32)
