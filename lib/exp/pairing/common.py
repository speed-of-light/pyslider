import numpy as np
import pandas as pd
from data_tuner import _DataTuner as Datn


class _Common(Datn):
    _mkeys = ["ski", "fki", "iix", "dist"]

    _epre = np.array([dict(en="BBF .7", ev=dict(bbft=0.7001)),
             dict(en="BBF .8", ev=dict(bbft=0.8001)),
             dict(en="BBF .9", ev=dict(bbft=0.9001)),
             dict(en="Raw Matches", ev=dict(bbft=1.0001)),
             dict(en="Ransac(1px)", ev=dict(bbft=1.0001, ransac=1.0)),
             dict(en="Ransac(5px)", ev=dict(bbft=1.0001, ransac=5.0)),
             dict(en="Ransac(10px)", ev=dict(bbft=1.0001, ransac=10.0)),
             dict(en="Ransac(20px)", ev=dict(bbft=1.0001, ransac=20.0)),
             dict(en="BBF(.8)\nRansac(5px)", ev=dict(bbft=.80001, ransac=5.0)),
             dict(en="BBF(.8)\nRansac(5px)\nHG", ev=dict(bbft=.80001, ransac=5.0, homo=True)),
             dict(en="BBF(.8)\nRansac(5px)\nHG\nOct", ev=dict(bbft=.80001, ransac=5.0, homo=True, octaf=1))
            ])

    def __init__(self):
        """
        Handling common process
        """
        Datn.__init__(self)

    def warmup(self):
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
        fos = "d{}_r{}_h{}_o{}"
        return fos.format(nds, ras, hos, oca)

    def __df_key(self, prefx="rs", data={"en":"default", "ev":None}):
        en = data["en"]
        ev = data["ev"]
        if ev is None:
            ev = dict(bbft=self.nn_dist, ransac=self.ransac,
                        homo=self.homo, octaf=self.octaf)
        rk = prefx + "_" + self.__df_key_base(**ev)
        return en, rk

    def _update_klass_var(self):
        kls = "{}_{}".format(self.featx.klass_var, self.mcore)
        self.klass_var = kls
        self.elog.info("Current configs: {}".format(kls))

    def _save_stats(self, prefx="rs", rdl=None):
        rdf = pd.DataFrame(rdl)
        en, st = self.__df_key(prefx)
        self.save(st, rdf)
        ins = "Save to {}.h5 with key: {}".format(self.klass_var, st)
        self.elog.info(ins)
        return rdf

    def __keyset(self, keys):
        if len(keys) == 0:
            keys = range(len(self._epre))
        kb = lambda dx: self.__df_key("rs", dx)
        return map(kb, self._epre[keys])

    def __load_and_proc(self, key, proc):
        data = self.load(key)
        if proc:
            data = proc(data)
        return data

    def iter_data(self, keys=[], proc=None):
        self._update_klass_var()
        for kn, ks in self.__keyset(keys):
            yield kn, self.__load_and_proc(ks, proc)
