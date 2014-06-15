import datetime as dt
from multiprocessing import Process, Queue, Lock
from memory_profiler import memory_usage as mu
import cv2
import pandas as pd
import time
# plotting
from matplotlib import offsetbox as ofb
# core
from base import ExpCommon
from tools.video import Video
from tools.slider import Slider
from tools.timer import ExpTimer


class Prepare(ExpCommon):
    """
    Data preprocessing class
    """
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.statq = self.cmdq = self.p = None
        ExpCommon.__init__(self, root, name)

    def share_data(self, data):
        sq = self.statq
        if sq is None:
            return
        if sq.full():
            sq.get()
        sq.put_nowait(data)

    def get_cmd(self):
        cq = self.cmdq
        if cq is None:
            return
        cmd = None
        if not cq.empty():
            cmd = cq.get_nowait()
        return cmd

    def diff(self, key='base', end=-1, size=2):
        vid = Video(self.vid)
        fps = vid.cap['fps']
        ret = []
        bgm = cv2.BackgroundSubtractorMOG(10, 6, 0.9, .1)
        vframes = vid.scoped_frames(start=0, end=end,
                                    size=2, time_span=1000/fps)
        for il in vframes:
            fgmask = bgm.apply(il[0]['img'])
            data = [il[0]['ms'], il[0]['fn'], fgmask.sum()]
            ret.append(data)
        return ret

    def diff_base(self, lock, key='base', end=-1, size=2):
        vid = Video(self.vid)
        fps = vid.cap['fps']
        seconds = vid.cap['seconds']
        end = vid.cap['seconds'] if (end == -1 or end > seconds) else end
        ret = []
        ts = 1000/fps
        for il in vid.scoped_frames(start=0, end=end, size=size, time_span=ts):
            data = yield(il)
            ret.append(data)
            self.share_data(dict(prog=il[0]['ms']/(1000*end)))
            if self.get_cmd() == 'stop':
                print "Process terminated at frame {}".format(il[0]['fn'])
                break
        df = pd.DataFrame(ret, columns=['ms', 'frame_id', 'diff'])
        self.share_data(dict(prog=1.0))
        if lock is not None:
            lock.acquire(timeout=180)
            self.save_to("diff_{}".format(key), df)
            lock.release()

    def diff_next(self, lock, end=-1, size=2):
        dk = "next/size_{}".format(size)
        fdb = self.diff_base(lock, key=dk, end=end, size=size)
        il = fdb.next()
        while il:
            ratio = 1.0/len(il)
            mix = il[0]['img']
            mix = cv2.addWeighted(mix, ratio, mix, 0, 0)
            for i, img in enumerate(il):
                if i == 0:
                    continue
                mix = cv2.addWeighted(mix, 1, img['img'], ratio, 0)
            suma = cv2.absdiff(il[-1]['img'], mix).sum()
            data = [il[0]['ms'], il[0]['fn'], suma]
            try:
                il = fdb.send(data)
            except StopIteration:
                break

    def diff_bkg(self, lock, end=-1, hist=30, bgr=0.9, nog=5, nr=.1):
        bgm = cv2.BackgroundSubtractorMOG(hist, nog, bgr, nr)
        # TODO: dfk does not support keys like 3.x test.name etc..
        dfk = "bkg/hist_{}/bgr_{}/nog_{}/nr_{}".format(hist, bgr, nog, nr)
        fdb = self.diff_base(lock, key=dfk, end=end)
        il = fdb.next()
        while il:
            fgmask = bgm.apply(il[0]['img'])
            data = [il[0]['ms'], il[0]['fn'], fgmask.sum()]
            try:
                il = fdb.send(data)
            except StopIteration:
                break

    def stop(self):
        if self.idle():
            return
        self.cmdq.put_nowait("stop")
        proc = self.p
        while not self.statq.empty():
            time.sleep(2)
            self.statq.get_nowait()
        if proc and proc.is_alive():
            proc.join()
            proc.terminate()

    def idle(self):
        balive = self.p and self.p.is_alive()
        sqnpt = self.statq and self.statq.empty()
        cqnpt = self.cmdq and self.cmdq.empty()
        return not (balive and sqnpt and cqnpt)

    def cap_vital_frame(self, byfunc, **kwargs):
        def func(*args, **kwa):  # unwrap function for local use
            for kw in kwa['kw_list']:
                fn = kw['fn']
                parl = kw['params']
                for par in parl:
                    with ExpTimer(verbose=True) as t:
                        # byfunc(*args, **kw)
                        mus = mu((fn, args, par), interval=.0,
                                 timeout=None, max_usage=False)
                    self.finq.put_nowait(dict(keys=par, name=fn.__name__,
                                              mem=mus[0], time=t.msecs))
            self.current_job = None

        if not self.idle():
            print "{} is working for {}".format(self.path, self.p.name)
            return
        lock = Lock()
        self.statq = Queue(3)
        self.cmdq = Queue(5)
        self.finq = Queue(500)
        self.p = Process(target=func, args=(lock,), kwargs=kwargs)
        self.p.start()

    def plot_annote(self, ax, raw, gnd, nodes, ffrom=0, fto=2000):
        """
        `ax`: axes for plot area
        `raw`: raw data for observation
        `gnd`: ground truth data
        `nodes`: nodes dict contained
          (index array, value array, text array) for marking
          important data.
        `section`: data range to display
        `window_size`: data size to display
        """
        def add_artist(ax, fid, pval, bounce=(.5, .5), img=None):
            if img is None:
                img = vid.get_frame(by='id', value=fid)
            oft = ofb.OffsetImage(img, zoom=0.1)
            boxp = dict(boxstyle='round,pad=0.1', ec='g')
            arrp = dict(arrowstyle="->", color='g')
            ab = ofb.\
                AnnotationBbox(oft, (fid, pval), xycoords='data', xybox=bounce,
                               boxcoords=('axes fraction', "axes fraction"),
                               bboxprops=boxp, arrowprops=arrp)
            ax.add_artist(ab)
        vid = Video(self.root, self.name)
        slid = Slider(self.name, self.root)
        xlim = (ffrom, fto)
        # plot diff value
        ln_raw = ax.plot(raw, color='black')
        ln_peak = ax.plot([ii['index'] for ii in nodes],
                          [vv['value'] for vv in nodes], 'ro')
        # plot ground truth
        ax2 = ax.twinx()
        ln_gnd = ax2.plot(gnd['fid'], gnd['sid'], 'b-')
        rng_sid = gnd[(gnd['fid'] > ffrom) & (gnd['fid'] < fto)].sid
        ax2.set_ylim(rng_sid.min()-1, rng_sid.max() + 1)
        ax.set_xlim(xlim)
        # make legend
        lns = ln_raw + ln_peak + ln_gnd
        # labs = [l.get_label() for l in lns]
        ax.legend(lns, ['raw', 'peak', 'ground'], loc=0)
        for nod in nodes:
            inx = nod['index']
            nov = nod['value']
            gsid = int(nod['gsid'])
            if inx < xlim[0]:
                continue
            if inx > xlim[1]:
                break
            frac = (inx-ffrom)*1.0/(fto-ffrom)
            add_artist(ax, inx - 1, nov, (frac-0.05, .65))
            # last
            add_artist(ax, inx, nov, (frac, .95))
            add_artist(ax, inx, nov, (frac, .05), img=slid.get_slide(gsid))
            oft = ofb.TextArea("{}[{}]".format(inx, gsid))
            boxp = dict(boxstyle='round,pad=0.1', ec='g')
            ab = ofb.\
                AnnotationBbox(oft, (inx, nov), xycoords='data',
                               xybox=(inx, 0.90), bboxprops=boxp,
                               boxcoords=('data', "axes fraction"),
                               arrowprops=dict(arrowstyle="->", color='g'))
            ax.add_artist(ab)
            # last
            add_artist(ax, inx + 1, nov, (frac+0.05, .8))

    def save_dfkeys(self):
        ss = self.store()
        sks = ss.keys()
        ss.close()
        kv = []
        for sk in sks:
            kv.append(self._args_from(sk))
        cols = ['key', 'method', 'arg1', 'arg2', 'arg3', 'arg4']
        kdf = pd.DataFrame(data=kv, columns=cols)
        sp = self.make('stores', 'h5', asure=True, root=False)
        kdf.to_hdf(sp, 'keys', mode='a', data_columns=True,
                   format='t', complib='blosc', complevel=self.comp)

    def save_reduced_fr(self):
        df = self.load('keys')
        i = 0
        with ExpTimer(verbose=0) as ts:
            for key in df['key'].values:
                if 'diff' not in key:
                    continue
                try:
                    adf = self.load(key)
                    bdf = adf[adf['diff'].gt(adf['diff'].quantile(.75))]
                    cdf = self._fr_reduce(bdf)
                    rk = '/reduce'+key
                    self.save(rk, cdf)
                    self.elog.info("{}-{}, {}, {}, rate: {}".
                                   format(rk, len(adf), len(bdf), len(cdf),
                                          len(adf)*1.0/len(cdf)))
                    i = i+1
                    if i > 8:
                        break
                except Exception, e:
                    ddn = str(dt.datetime.now())
                    err = "At {}:\r\n {}".format(ddn, e)
                    self.notify(err)
                    self.log.error(err)
        self.notify("Finished, spent time: {}".format(ts.tstr()))

    def _args_from(self, key):
        """
        Split key string into list of array
        """
        va = [key]
        for ks in key.split('/'):
            if ks is '':
                continue
            if 'diff' in ks:
                va.append(ks)
            else:
                va.append(float(ks.split('_')[1]))
        return va

    def _fr_reduce(self, df):
        """
        Keep max value in each continued sequence.
        ex:
         index = [ 1, 2, 3, 4, 7, 8, 9, 12, 13]
         value = [ 4, 2, 3, 3, 5, 8, 7,  8,  9]
         =>
         index = [ 1, 8, 13]
         value = [ 4, 8,  9]
        """
        igmax = -1
        last_v = -1
        for i, v in enumerate(df.index):
            if i == 0:
                igmax = v
                continue
            if (v - last_v) == 1:  # check conti series max
                if df.ix[igmax]['diff'] < df.ix[v]['diff']:
                    df = df.drop([igmax])
                    igmax = v
                else:
                    df = df.drop([v])
            else:
                igmax = v
            last_v = v
        return df
