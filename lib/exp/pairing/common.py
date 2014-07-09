import pandas as pd


class _Common(object):
    _mkeys = ["ski", "fki", "iix", "dist"]
    _skeys = ["sid", "fid", "time", "dlen", "mean_dist",
              "qart_dist", "top10_dist"]

    def __init__(self):
        """
        Handling common process
        """
        pass

    def warmup(self):
        self.set_default_vars()
        self.set_featx()
        self.set_matcher()

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

    def _statisticalize(self, data, timer, frame=None, slide=None):
        time = timer.msecs
        dlen = len(data)
        mdis = data.dist.mean()
        qcond = data["dist"] < data["dist"].quantile(.25)
        qdis = data[qcond].dist.mean()
        tdis = data.sort(columns="dist")[:10].mean()
        raw = [slide["pid"], frame["pid"], time, dlen, mdis, qdis, tdis]
        return dict(zip(self._skeys, raw))

    def __pair_key(self, sid, fid):
        return "m_{:03d}_{:03d}".format(sid, fid)

    def _save_pdf(self, pdf, slide=None, frame=None):
        # TODO move update klass var out of this
        mk = self.__pair_key(slide["pid"], frame["pid"])
        self.save(mk, pdf)

    def _save_rtlog(self, rdl):
        rdf = pd.DataFrame(rdl)
        self.save("rtlog", rdf)

    def __pdf_key(self):
        nds = "{:2.0f}".format(self.nn_dist*100)
        ras = "{:2.0f}".format(self.ransac*100) if self.ransac else "NoRansac"
        hos = "homo" if self.homo else "NoHomo"
        return "{}_{}_{}".format(nds, ras, hos)

    def _update_klass_var(self):
        kls = "{}_{}".format(self.featx.klass_var, self.mcore)
        st = self.__pdf_key()
        self.klass_var = "{}_{}".format(kls, st)
        self.elog.info("Current configs: {}".format(st))

