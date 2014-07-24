import pandas as pd
from lib.exp.evaluator.ground_truth import GroundTruth


class SlideVoter(object):
    voter = ["fid", "gnd", "area", "top50", "mean",
             "rmean", "invr"]
    def __init__(self, root, name, ssf):
        """
        ssf: slide to slide feats matrix
        """
        self.gnd = GroundTruth(root, name)
        self.ssf = ssf

    def __make_votes(self, data):
        fi, fd = data[0], data[1]
        sids = [fi, self.gnd.answer(fi)]
        sids.append(int(fd.ix[fd[fd.area_ratio < 1.5].area_ratio.argmax()].sid))
        sids.append(int(fd.ix[fd.top50.argmin()].sid))
        sids.append(int(fd.ix[fd.mean_dist.argmin()].sid))
        sids.append(int(fd.ix[fd.rtop10.argmin()].sid))
        sids.append(int(fd.ix[fd.inv_rdist.argmin()].sid))
        return sids

    def __invite_voters(self, fdf):
        vrs = map(self.__make_votes, fdf.groupby("fid"))
        return pd.DataFrame(vrs, columns=self.voter)

    def __even_weight(self, cnt):
        return [1./cnt]*cnt

    def __voting(self, vl, w):
        return vl*w

    def __prepare(self, cdf, pdf):
        xdf = cdf[cdf.bot_area_ans == 0]
        fids = [xi for xi, xd in xdf.groupby("fid")]
        return pdf[pdf.fid.isin(fids)]

    def votes(self, cdf, pdf, voters=["area"], name="area_only"):
        df = self.__prepare(cdf, pdf)
        vdf = self.__invite_voters(df)
        vok = "{}_ans".format(name)
        vw = self.__even_weight(len(voters))
        vdf[vok] = self.__voting(vdf[voters].values, vw)
        return vdf
