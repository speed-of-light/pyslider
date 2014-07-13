import pandas as pd
from data_tuner import _DataTuner as Datn


class _Common(Datn):
    _mkeys = ["ski", "fki", "iix", "dist"]

    def __init__(self):
        """
        Handling common process
        """
        Datn.__init__(self)

    def warmup(self):
        self.set_default_vars()
        self.set_featx()
        self.set_matcher()

    def __pair_key(self, sid, fid):
        return "m_{:03d}_{:03d}".format(sid, fid)

    def _save_pdf(self, pdf, slide=None, frame=None):
        # TODO move update klass var out of this
        mk = self.__pair_key(slide["pid"], frame["pid"])
        self.save(mk, pdf)

    def __df_key_base(self, bbft=.9, ransac=None, homo=False, octaf=0):
        nds = "{:2.0f}".format(bbft*100)
        ras = "{:2.0f}".format(ransac*100) if ransac else "NoRansac"
        hos = "homo" if homo else "NoHomo"
        oca = "{:d}".format(octaf)
        fos = "rs_d{}_r{}_h{}_o{}"
        return fos.format(nds, ras, hos, oca)

    def __df_key(self):
        kbs = self.__df_key_base(self.nn_dist, self.ransac, self.homo,
                                 self.octaf)
        return kbs

    def _update_klass_var(self):
        kls = "{}_{}".format(self.featx.klass_var, self.mcore)
        self.klass_var = kls
        self.elog.info("Current configs: {}".format(kls))

    def _save_stats(self, rdl):
        rdf = pd.DataFrame(rdl)
        st = self.__df_key()
        self.save(st, rdf)
        ins = "Save to {}.h5 with key: {}".format(self.klass_var, st)
        self.elog.info(ins)
        return rdf

    def cfg_keys(self, bbftv=[]):
        kb = self.__df_key_base
        return map(kb, bbftv)
