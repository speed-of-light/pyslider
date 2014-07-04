import numpy as np
from lib.exp.filters.ransac import Ransac
from core import Plotter


class FrameSlidesBar(Plotter):
    def __init__(self):
        """
        Plot frame and slides, distance
        """
        Plotter.__init__(self)

    def __autolabel(self, ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height,
                    '%d' % int(height), ha='center', va='bottom')

    def __labling(self, ax, fid):
        ax.set_title("Distance of all slides and frame#{}".format(fid))
        ax.set_xlabel("Slide ID")
        ax.set_ylabel("Distance")
        ax.legend()

    def __get_data(self, matches):
        x = [m['sid'] for m in matches]
        y = [m['df'].dist.mean() for m in matches]
        ystd = [m['df'].dist.std() for m in matches]
        return x, y, ystd

    def __base_bars(self, ax, x, y, ystd, w, color="#98AEDa"):
        rects = ax.bar(x, y, color=color, yerr=ystd, ecolor='b', width=w)
        self.__autolabel(ax, rects)

    def __min_bar(self, ax, x, y, w):
        myi = min(xrange(len(y)), key=y.__getitem__) + 1
        ax.bar([myi+x], min(y), color='#66EE33', label="Min (Predicted)",
               width=w)

    def __ans_bar(self, ax, gnd, fid, y, w):
        x = gnd.answer(fid)
        ax.bar([x], y[x-1]/2, color='#DE5344', label="GoundTruth", width=w)

    def __matching_bars(self, ax, matches, gnd, fid, w=1):
        x, y, ystd = self.__get_data(matches)
        self.__base_bars(ax, x, y, ystd, w)
        self.__min_bar(ax, 0, y, w)
        self.__ans_bar(ax, gnd, fid, y, w)

    def __fitered_data(self, matchx):
        ra = Ransac(matchx)
        fm = []
        for mm in matchx.matches:
            m, mask = ra.filter_pair(**mm)
            fm.append(dict(sid=mm['sid'], fid=mm['fid'],
                           df=mm['df'][mask == 1]))
        return fm

    def __filtered_bars(self, ax, matchx, w=0.45):
        fm = self.__fitered_data(matchx)
        x, y, ystd = self.__get_data(fm)
        xw = np.array(x)+w+0.01
        self.__base_bars(ax, xw, y, ystd, w, "#EE99BB")
        self.__min_bar(ax, w+0.01, y, w)

    def frame_slides_bars(self, ax, fid, gnd, matchx):
        self.__matching_bars(ax, matchx.matches, gnd, fid, w=0.9)
        self.__labling(ax, fid)

    def frame_slides_wfbars(self, ax, fid, gnd, matchx):
        self.__matching_bars(ax, matchx.matches, gnd, fid, w=0.4)
        self.__filtered_bars(ax, matchx, w=0.44)
        self.__labling(ax, fid)

    def batch_bars(self, fig, matchx, gnd, start=0, size=-1):
        fids = matchx.frame_seeds()
        fids = fids[start: start+size]
        for fii, fid in enumerate(fids, 1):
            ax = fig.add_subplot(len(fids), 1, fii)
            matchx.frame_matches(fid, thres=1.1, auto_save=False)
            self.frame_slides_wfbars(ax, fid, gnd, matchx)
