class _TexCom(object):
    def _emphasis(self, thres=.99, ks="emphasis", val=None):
        if (val is not None) & (val > thres):
            bs = "BL{:.3f}BR".format(val)
            tc = "STextcolorBL{}BR{}".format(ks, bs)
            it = "STextitBL{}BR".format(tc)
        else:
            it = "{:.3f}".format(val)
        return it

    def _bold_text(self, key="Bot Area Ans", val=None):
        if (val == key):
            bs = "STextbfBL{}BR".format(val)
        else:
            bs = val
        return bs

    def _fmts(self):
        bbaa = lambda v: self.__bold_text(val=v)
        emph = lambda v: self.__emphasis(val=v, thres=.95)
        noti = lambda v: self.__emphasis(val=v, thres=.9, ks="notify")
        return dict(
            key=bbaa,
            sensitivity=emph, accuracy=noti,
            precision=noti, speficity=noti)

    def _repl_base(self, ts):
        ts = ts.replace("BL", "{")
        ts = ts.replace("BR", "}")
        ts = ts.replace("ST", "\\t")
        return ts
