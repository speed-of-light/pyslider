import numpy as np
import pandas as pd
from data_tuner import _DataTuner as Datn


class _Common(Datn):
    def __init__(self):
        """
        Handling common process
        """
        Datn.__init__(self)
        self._epre = self.__preset_conf()

    def __fix_base(self, pre, vals, bd, key, fmt):
        pf = lambda n: fmt.format(pre, n)
        names = map(pf, vals)
        vset = []
        for v in vals:
            bd[key] = v
            vset.append(bd.copy())
        return names, vset

    def __fix_bbft(self):
        n, v = self.__fix_base(
            "BBF", np.arange(.7001, 1.001, .1), dict(), "bbft", "{}({:.1f})")
        return map(self.__preset, n, v)

    def __fix_ransac(self, bbft=1.001):
        n, v = self.__fix_base(
            "Ransac", [1., 5., 10., 20.], dict(bbft=bbft),
            "thres", "{}({:.0f}px)")
        return map(self.__preset, n, v)

    def __fix_invw(self, bbft=.8, ransac=5.0):
        n, v = self.__fix_base("InvRansac", [1, 2, 3],
                               dict(bbft=bbft, thres=ransac), "invw", "{}(^{})")
        return map(self.__preset, n, v)

    def __preset_conf(self):
        ca = self.__fix_bbft()
        ca += self.__fix_ransac()
        ca += self.__fix_ransac(bbft=.8)
        ca += self.__fix_invw(bbft=.8, ransac=5.0)
        ca += self.__fix_invw(bbft=.8, ransac=10.0)
        return np.array(ca)

    def __preset(self, name="default", kwargs=dict()):
        base = dict(
            bbft=0.9, thres=0, homo=False, mm=10, area=True,
            invw=0, octaf=0)
        base.update(kwargs)
        return dict(en=name, ev=base)

    def warmup(self):
        self.set_featx()
        self.set_matcher()
        self._update_klass_var()

    def __pair_key(self, sid, fid):
        return "m_{:03d}_{:03d}".format(sid, fid)

    def _save_pdf(self, pdf, sx=None, fx=None):
        # TODO move update klass var out of this
        mk = self.__pair_key(sx["pid"], fx["pid"])
        self.save(mk, pdf)

    def __df_key_base(self, **dt):
        bs = "d{:2.0f}".format(dt["bbft"]*100)
        bs += "_ra{:2.0f}".format(dt["thres"]*100) if dt["thres"] else "_NoRansac"
        bs += "_rm{:d}".format(dt["mm"])
        bs += "_iw{:d}".format(dt["invw"])
        bs += "_ot{:d}".format(dt["octaf"])
        bs += "_Homo" if dt["homo"] else "_NoHomo"
        bs += "_Area" if dt["area"] else "_NoArea"
        return bs

    def __df_key(self, prefx="rs", data={"en": "default", "ev": None}):
        en = data["en"]
        ev = data["ev"]
        if ev is None:
            ev = self._configs()
        rk = prefx + "_" + self.__df_key_base(**ev)
        return en, rk

    def _update_klass_var(self):
        kls = "{}_{}".format(self.featx.klass_var, self.mcore)
        self.klass_var = kls
        self.elog.info("Current configs: {}".format(kls))

    def _save_stats(self, prefx="rs", rdl=None):
        rdf = pd.DataFrame(rdl)
        en, st = self.__df_key(prefx, dict(en="", ev=None))
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
        """
        yield "data name" and its data pack
        """
        self._update_klass_var()
        for kn, ks in self.__keyset(keys):
            yield kn, self.__load_and_proc(ks, proc)

    def dp_group_fid(self, data):
        dgs = data.groupby("fid")
        ad = [self.__group_dist(*dg) for dg in dgs]
        return pd.DataFrame(ad)
