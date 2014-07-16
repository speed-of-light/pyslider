import pandas as pd


class _DataTuner(object):
    _skeys = ["sid", "fid", "time", "dlen", "olen",
              "mean_dist", "qart_dist", "top10_dist",
              ]

    def __init__(self):
        """
        Output integrated useful data information
        """
        pass

    def _to_matches_df(self, data):
        """
        `ski`: slide keypoint index
        `fki`: frame keypoint index
        """
        if len(data) is 0:
            df = pd.DataFrame(columns=self._mkeys)
        else:
            dflator = lambda m: [m.queryIdx, m.trainIdx, m.imgIdx, m.distance]
            fm = map(dflator, data)
            df = pd.DataFrame(fm, columns=self._mkeys)
        return df

    def __base_dist(self, data):
        if len(data) == 0:
            return [None, None, None]
        mdis = data.dist.mean()
        qcond = data["dist"] < data["dist"].quantile(.25)
        qdis = data[qcond].dist.mean()
        tdis = data.sort(columns="dist")[:10].dist.mean()
        return [mdis, qdis, tdis]

    def _statisticalize(self, data=None, olen=None, timer=None, frame=None,
                        slide=None):
        aa = [slide["pid"], frame["pid"]]
        aa += [timer.msecs, len(data), olen]
        aa += self.__base_dist(data)
        return dict(zip(self._skeys, aa))

    def __group_dist(self, gi, grp):
        r = dict(fid=gi,
                 mean_dist=grp.mean_dist.mean(),
                 qart_dist=grp.qart_dist.mean(),
                 top_dist=grp.top10_dist.mean())
        return r

    def dp_group_fid(self, data):
        dgs = data.groupby("fid")
        ad = [self.__group_dist(*dg) for dg in dgs]
        return pd.DataFrame(ad)
