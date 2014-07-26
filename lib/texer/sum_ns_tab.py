class SumNsTab(object):
    def __init__(self, data):
        self.df = data

    def __mark_loc_best(self):
        for df in self.df:
            df["local_best"] = 0
            for ti, tg in df.groupby("key"):
                ix = tg.sort(columns=["sensitivity", "precision", "accuracy", "sensitivity"], ascending=False).iloc[0].name
                df.ix[ix, "local_best"] = 1

    def __concat_best(self):
        skey = ["Mean Ans", "Top50 Ans", "Ridist Ans", "Bot Area Ans", "Rdist Ans"]
        dp = None
        for df in self.df:
            dff = df[(df["local_best"] == 1) & df.key.isin(skey)]
            dp = dff if dp is None else dp.append(dff)
        return dp

    def __dp(self):
        self.__mark_loc_best()
        dp = self.__concat_best()
        return dp.sort(columns=["sensitivity"], ascending=False)

    def __emphasis(self, thres=.99, ks="emphasis", val=None):
        if (val is not None) & (val > thres):
            bs = "BL{:.3f}BR".format(val)
            tc = "STextcolorBL{}BR{}".format(ks, bs)
            it = "STextitBL{}BR".format(tc)
        else:
            it = "{:.3f}".format(val)
        return it

    def __bold_text(self, key="Bot Area Ans", val=None):
        if (val == key):
            bs = "STextbfBL{}BR".format(val)
        else:
            bs = val
        return bs

    def __fmts(self):
        bbaa = lambda v: self.__bold_text(val=v)
        emph = lambda v: self.__emphasis(val=v, thres=.95)
        noti = lambda v: self.__emphasis(val=v, thres=.9, ks="notify")
        return dict(
            key=bbaa,
            sensitivity=emph, accuracy=noti,
            precision=noti, speficity=noti)

    def __repl_base(self, ts):
        ts = ts.replace("BL", "{")
        ts = ts.replace("BR", "}")
        ts = ts.replace("ST", "\\t")
        return ts

    def __post_repl(self, st):
        ts = self.__repl_base(st)
        ts = ts.replace("Bot", "Top")
        ts = ts.replace(" Ans", "")
        ts = ts.replace("dsn", "DataSet")
        ts = ts.replace("key", "Key")
        ts = ts.replace("sensi", "Sensi")
        ts = ts.replace("preci", "Preci")
        ts = ts.replace("accuracy", "Accuracy")
        ts = ts.replace("speci", "Speci")
        return ts

    def __fmt_base(self, df):
        cols = ["dsn", "key", "sensitivity", "precision", "accuracy", "speficity"]
        fmts = self.__fmts()
        st = df.to_latex(columns=cols, formatters=fmts, index=0)
        st = self.__post_repl(st)
        return st

    def tabular(self):
        dp = self.__dp()
        st = self.__fmt_base(dp)
        return st
