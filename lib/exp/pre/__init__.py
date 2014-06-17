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

from lib.exp.base import ExpCommon


class Reducer(ExpCommon):
    def __init__(self, root, name):
        ExpCommon.__init__(self, root, name)

    def __compress(self, data):
        """
        Get the compressed dataset and compressed ratio
        """
        before = len(data)
        igmax = data.iloc[0].index
        last_v = data.iloc[0].index
        for v in data.index[1:]:
            if (v - last_v) == 1:  # check conti series max
                if data.ix[igmax]['diff'] < data.ix[v]['diff']:
                    data = data.drop([igmax])
                    igmax = v
                else:
                    data = data.drop([v])
            else:
                igmax = v
            last_v = v
        return data, before, len(data)

    def __get_data(self, key):
        """
        Get probed `differenc` values and `frame` data
        """
        df = self.load(key)
        dmean = df.diff.mean()
        can = df[df.diff.gt(dmean)]
        return can

    def __results(self, **opts):
        after = opts["after"]
        before = opts["before"]
        info = "before: {}, after: {}, ratio: {}".\
            format(before, after, after*1.0/before)
        print "Reduce data from", info
        self.elog.info("Reduce data from", info)
        self.save_rtlog(opts.keys(), opts.values())

    def reduce(self, key):
        can = self.__get_data(key)
        red, before, after = self.__compress(can)
        self.__results(key=key, before=before, after=after)
        return red
