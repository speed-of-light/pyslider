class _DataTuner(object):
    _skeys = ["sid", "fid", "area_ratio",
              "time", "dlen", "olen",
              "mean_dist", "qart_dist",
              "top10", "top20", "top30", "top40", "top50",
              "rtop10", "rdist", "inv_rdist"
              ]

    def __init__(self):
        """
        Output integrated useful data information
        """
        pass

    def __no_data(self, data):
        return (len(data) == 0)

    def __no_ransac(self, data):
        return ("ransac" not in data.columns)

    def __datagen(func):
        def inner(self, *args, **kwargs):
            rejectable = kwargs["rejector"]
            if rejectable(args[0]):
                return [None]*kwargs["isize"]
            return func(self, *args, **kwargs)
        return inner

    @__datagen
    def __topN(self, data, isize=5, rejector=None):
        sd = data.sort(columns="dist")
        dm = lambda n: sd[:n].dist.mean()
        return map(dm, range(10, 10*(isize+1), 10))

    @__datagen
    def __base_dist(self, data, isize=2, rejector=None):
        mdis = data.dist.mean()
        qcond = data["dist"] < data["dist"].quantile(.25)
        qdis = data[qcond].dist.mean()
        return [mdis, qdis]

    @__datagen
    def __ransac_dist(self, data, isize=3, rejector=None):
        rdf = data[data.ransac > 0]
        ra = self.__topN(rdf, isize=5, rejector=self.__no_data)[:1]
        ra += [rdf.dist.mean()]
        dist = data.dist.copy()
        dist[dist == 0] = 1
        data["wd"] = dist * data["ransac"]
        ra += [data.wd.mean()]
        return ra

    def __arear(self, data):
        ar = None
        if "area" in data.columns:
            dar = data.iloc[0]
            ar = dar.area/dar.barea
        return ar

    def _statisticalize(self, data=None, olen=None, timer=None,
                        sx=None,  fx=None):
        aa = [sx["pid"], fx["pid"], self.__arear(data)]
        aa += [timer.msecs, len(data), olen]
        aa += self.__base_dist(data, isize=2, rejector=self.__no_data)
        aa += self.__topN(data, isize=5, rejector=self.__no_data)
        aa += self.__ransac_dist(data, isize=3, rejector=self.__no_ransac)
        return dict(zip(self._skeys, aa))

    def __group_dist(self, gi, grp):
        r = dict(fid=gi,
                 mean_dist=grp.mean_dist.mean(),
                 qart_dist=grp.qart_dist.mean(),
                 top_dist=grp.top10_dist.mean())
        return r

