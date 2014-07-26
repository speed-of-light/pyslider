from tex_com import _TexCom


class SumSfCovTab(_TexCom):
    def __init__(self, data):
        self.dc = data

    _cols = ["dsn", "key", "fslc", "fswc", "slc", "swc", "slcn", "swcn"]
    _conf = ["dsn", "key", "fslc", "fswc", "slc", "swc", "slcn", "swcn"]

    def __sdf(self):
        sdf = None
        scl = ["fslc", "fswc", "slc", "swc", "slcn", "swcn"]
        for ci, rg in self.dc.groupby("dsn"):
            sgf = rg.sort(columns=scl, ascending=False)[:5]
            sdf = sgf if sdf is None else sdf.append(sgf)
        sdf = sdf.sort(columns=["dsn", "fswc", "fslc", "key"])
        return sdf[self._cols]

    def __fmts(self):
        bbaa = lambda v: self._bold_text(val=v, key="bot_area")
        emph = lambda v: self._emphasis(val=v, thres=.9)
        return dict(
            key=bbaa,
            fslc=emph, fswc=emph,
            slc=emph,swc=emph)

    def __post_repl(self, st):
        st = st.replace("fswc", "STextbfBLswcBR")
        st = st.replace("fslc", "STextbfBLslcBR")
        st = st.replace("slc", "Slide")
        st = st.replace("swc", "Switch")
        st = st.replace("slcn", "SL.")
        st = st.replace("swcn", "SW.")
        st = st.replace("dsn", "Dataset")
        st = st.replace("key", "Key")
        st = st.replace("_ans", "")
        st = st.replace("v_", "")
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
