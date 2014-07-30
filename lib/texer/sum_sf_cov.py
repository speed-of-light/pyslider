from tex_com import _TexCom


class SumSfCovTab(_TexCom):
    def __init__(self, data):
        self.dc = data

    _cols = ["dsn", "key", "fslc", "fswc", "slc", "swc", "slcn", "swcn"]
    _accs = ["dsn", "key", "accuracy", "precision", "sensitivity", "speficity"]

    def __sdf(self):
        sdf = None
        scl = ["fslc", "fswc", "slc", "swc", "slcn", "swcn"]
        for ci, rg in self.dc.groupby("dsn"):
            sgf = rg.sort(columns=scl, ascending=False)[:5]
            sdf = sgf if sdf is None else sdf.append(sgf)
        sdf = sdf.sort(columns=["dsn", "fswc", "fslc", "key"])
        return sdf

    def __fmts(self):
        bbaa = lambda v: self._bold_text(val=v, key="iaaa")
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
        st = st.replace("\\_ans", "")
        st = st.replace("v\\_", "")
        st = self._repl_base(st)
        return st

    def __texer(self, df):
        fmts = self.__fmts()
        st = df.to_latex(columns=self._cols, formatters=fmts, index=0)
        st = self.__post_repl(st)
        return st

    def __acc_fmts(self):
        bbaa = lambda v: self._bold_text(val=v, key="v_atm")
        emph = lambda v: self._emphasis(val=v, thres=.8)
        return dict(
            key=bbaa,
            accuracy=emph, precision=emph,
            sensitivity=emph, speficity=emph)

    def __acc_repl(self, st):
        st = st.replace("accuracy", "Accuracy")
        st = st.replace("precision", "Precision")
        st = st.replace("sensitivity", "Sensitivity")
        st = st.replace("speficity", "Speficity")
        st = st.replace("dsn", "Dataset")
        st = st.replace("key", "Key")
        st = st.replace("\\_ans", "")
        st = st.replace("v\\_", "")
        st = self._repl_base(st)
        return st

    def __acc_texer(self, df):
        fmts = self.__acc_fmts()
        df = df.sort(columns=["dsn", "accuracy", "precision", "sensitivity", "speficity"])
        st = df.to_latex(columns=self._accs, formatters=fmts, index=0)
        st = self.__acc_repl(st)
        return st

    def tabular(self, cov):
        df = self.__sdf()
        if cov:
            st = self.__texer(df)
        else:
            st = self.__acc_texer(df)
        return st
