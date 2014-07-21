import pandas as pd


class NsfRocTab(object):
    def __init__(self):
        pass

    def __extreme(self, data, key):
        di = data[key].argmax()
        return data.ix[di]

    def __bold_max(self, dseries, x):
        if dseries.max() - x < 0.000001:
            bs = "BL{:.3f}BR".format(x)
            tc = "STextcolorBLemphasisBR{}".format(bs)
            it = "STextitBL{}BR".format(tc)
        else:
            it = "{:.3f}".format(x)
        return it

    def __tex_post(self, txt):
        txt = txt.replace("ST", "\\t")
        txt = txt.replace("BL", "{")
        txt = txt.replace("BR", "}")
        return txt

    def __tex_roc_table(self, data):
        res = ["name", "key", "sensitivity", "precision", "accuracy"]
        fmts = dict(
            header=lambda x: x[:3],
            accuracy=lambda x: self.__bold_max(data["accuracy"], x),
            precision=lambda x: self.__bold_max(data["precision"], x),
            sensitivity=lambda x: self.__bold_max(data["sensitivity"], x))
        ffmt = "{:3,.3f}".format
        st = data.to_latex(columns=res, index=0, formatters=fmts,
                           float_format=ffmt)
        return self.__tex_post(st)

    def tabular(self, data):
        df = pd.DataFrame()
        df = df.append(self.__extreme(data, "sensitivity"))
        df = df.append(self.__extreme(data, "precision"))
        df = df.append(self.__extreme(data, "accuracy"))
        return self.__tex_roc_table(df)
