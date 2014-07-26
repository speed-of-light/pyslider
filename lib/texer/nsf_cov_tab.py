class NsfCovTab(object):
    def __init__(self):
        pass

    def __rep_cusmarks(self, ts):
        """
        replace customed marks
        """
        ts = ts.replace("BL", "{")
        ts = ts.replace("BR", "}")
        ts = ts.replace("ST", "\\t")
        return ts

    def __rep(self, ts):
        ts = self.__rep_cusmarks(ts)
        ts = ts.replace("fix\_", "On-job ")
        ts = ts.replace(" slc ", "Slide Cov.")
        ts = ts.replace(" swc ", "Switches Cov.")
        ts = ts.replace(" key ", "Classifier")
        ts = ts.replace(" ic ", "Matcher")
        ts = ts.replace("bot\_area", "Top Area")
        return ts

    def __note_oval(self, val):
        if val > 0.99:
            bs = "BL{:.3f}BR".format(val)
            tc = "STextcolorBLemphasisBR{}".format(bs)
            it = "STextitBL{}BR".format(tc)
        else:
            it = "{:.3f}".format(val)
        return it

    def __texer(self, data, cols):
        nov = self.__note_oval
        ts = data.to_latex(columns=cols, index=0,
                         formatters=dict(slc=nov, swc=nov, fix_slc=nov, fix_swc=nov),
                         float_format="{:.3f}".format)
        return self.__rep(ts)

    def __prep_data(self, data, cols, sels):
        tdf = data.sort(columns=cols, ascending=False).iloc[sels]
        tdf['ic'] = "[" + tdf.index.astype(str) + "]" + tdf.config
        return tdf

    def tabular(self, sels, data):
        cols = ["slc", "swc", "fix_slc", "fix_swc"]
        df = self.__prep_data(data, cols, sels)
        cols.insert(0, "key")
        cols.insert(0, "ic")
        return self.__texer(df, cols)
