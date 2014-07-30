from tex_com import _TexCom


class SumNsCovTab(_TexCom):
    def __init__(self, data):
        self.dc = data

    _cols = ["dsn", "key", "fix_slc", "fix_swc", "slc", "swc", "sls", "sws"]

    def __sdf(self):
        sdf = None
        for fk in ["bot_area", "top50", "rdist"]:
            for gi, gd in self.dc.groupby("dsn"):
                sgf = gd.sort(columns=["fix_slc", "fix_swc", "slc", "swc", "key"], ascending=False)
                sgf = sgf[sgf.key == fk]
                sdf = sgf[:1] if sdf is None else sdf.append(sgf[:1])
        sdf = sdf.sort(columns=["key", "dsn"])
        sdf[self._cols]
        return sdf

    def __fmts(self):
        bbaa = lambda v: self._bold_text(val=v, key="bot_area")
        emph = lambda v: self._emphasis(val=v, thres=.95)
        return dict(
            key=bbaa,
            fix_slc=emph, fix_swc=emph,
            slc=emph, swc=emph)

    def __post_repl(self, st):
        st = st.replace("fix\\_swc", "STextbfBLswcBR")
        st = st.replace("fix\\_slc", "STextbfBLslcBR")
        st = st.replace("slc", "Slide Cov.")
        st = st.replace("swc", "Switch Cov.")
        st = st.replace("sls", "SL.")
        st = st.replace("sws", "SW.")
        st = st.replace("dsn", "Dataset")
        st = st.replace("key", "Key")
        st = st.replace("bot\\_area", "Top Area")
        st = st.replace("rdist", "RANSAC")
        st = st.replace("Top50", "RANSAC")
        st = self._repl_base(st)
        return st

    def __texer(self, df):
        fmts = self.__fmts()
        st = df.to_latex(columns=self._cols, formatters=fmts, index=0)
        st = self.__post_repl(st)
        return st

    def tabular(self):
        df = self.__sdf()
        st = self.__texer(df)
        return st
