import pandas as pd
from lib.exp.evaluator.ground_truth import GroundTruth


class SlideVoter(object):
    voter = ["fid", "gnd", "area", "top50", "mean",
             "rmean", "invr"]
    def __init__(self, root, name, cdf, pdf, ssf):
        """
        ssf: slide to slide feats matrix
        """
        self.gnd = GroundTruth(root, name)
        self.ssf = ssf
        df = self.__prepare(cdf, pdf)
        self.vdf = self.__invite_voters(df)

    def __make_votes(self, data):
        fi, fd = data[0], data[1]
        sids = [fi, self.gnd.answer(fi-30)]
        sids.append(int(fd.ix[fd[fd.area_ratio < 1.5].area_ratio.argmax()].sid))
        sids.append(int(fd.ix[fd.top50.argmin()].sid))
        sids.append(int(fd.ix[fd.mean_dist.argmin()].sid))
        sids.append(int(fd.ix[fd.rtop10.argmin()].sid))
        sids.append(int(fd.ix[fd.inv_rdist.argmin()].sid))
        return sids

    def __invite_voters(self, fdf):
        vrs = map(self.__make_votes, fdf.groupby("fid"))
        return pd.DataFrame(vrs, columns=self.voter)

    def __get_weight(self, wm, vc):
        if "even" in wm:
            return [1./vc]*vc
        elif len(wm) > 0:
            return wm

    def __vote(self, row, wm="even refine"):
        wdf = pd.DataFrame(row.values, columns=["sid"])
        wdf["w"] = self.__get_weight(wm, len(row.values))
        sid, conf = -1, 0
        for wi, wg in wdf.groupby("sid"):
            wgs = wg.w.sum()
            conf = wgs if wgs > conf else conf
            sid = wi if (wgs >= conf) & (wgs > .5) else sid
        return dict(ans=sid, confidence=conf)

    def __voting(self, vdf, w):
        vf = lambda vr: self.__vote(vr, w)
        vd = map(vf, [vr for vi, vr in vdf.iterrows()])
        return pd.DataFrame(vd)

    def __prepare(self, cdf, pdf):
        xdf = cdf[cdf.bot_area_ans == 0]
        fids = [xi for xi, xd in xdf.groupby("fid")]
        return pdf[pdf.fid.isin(fids)]

    def __refine(self, vdf, vf, vk):
        for vi in range(2, len(vf)-2):
            precf = vf.iloc[vi-2:vi].confidence.mean()
            poscf = vf.iloc[vi+1:vi+3].confidence.mean()
            vcr = vdf.iloc[vi]
            conf = vf.iloc[vi].confidence
            if (conf < 0.34) & (conf <= precf) & \
               (conf <= poscf) & (len(vcr.value_counts()) > 2):
                vf.ix[vf.iloc[vi].name, "ans"] = vcr.area

    def votes(self, voters=["area"], name="area_only", wts="even"):
        vok = "{}_ans".format(name)
        voc = "{}_conf".format(name)
        vf = self.__voting(self.vdf[voters], wts)
        if ("refine" in wts):
            self.__refine(self.vdf[voters], vf, vok)
        self.vdf[vok] = vf["ans"]
        self.vdf[voc] = vf["confidence"]
