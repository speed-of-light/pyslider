import numpy as np
import pandas as pd
import collections
import glob
import cv2
import cv


class Video(object):
    def __init__(self, root, name):
        """
        Author: speed-of-light
        Purpose: Operations on video frames
        """
        vid = glob.glob("./data/{}/{}/video.*".format(root, name))[0]
        self.stream_path = vid
        self.cap_loaded = False

    @property
    def __cap(self):
        if self.stream_path == "":
            return ""
        else:
            cap = cv2.VideoCapture(self.stream_path)
            fps = cap.get(cv.CV_CAP_PROP_FPS)
            frs = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
            ret = {
                "cap": cap,
                "fps": fps,
                "frames": frs,
                "seconds": frs/fps
            }
            return ret

    @classmethod
    def from_path(self, stream_path=""):
        self.stream_path = stream_path

    def scoped_frames(self, start=0, end=-1, size=1, time_span=1000):
        """
        Return a generator to manipulate with frames

        Parameters
        ----------
        start: millisecond
        end: millisecond, -1 to auto detect
        size: scoped size to dump frames
        time_span: 1000ms

        Returns
        -------
        Image and it's timestamp in milliseconds
        """
        if self.cap == "":
            yield None, None
        capr = self.cap
        cap = capr['cap']
        i = 0 if start < 0 else start
        fin = capr['seconds'] if (end == -1 or end > capr['seconds']) else end
        fin = fin * 1000  # time range in ms
        iset = collections.deque([])
        while True:
            k = i*time_span
            if k > fin:
                break
            cap.set(cv.CV_CAP_PROP_POS_MSEC, k)
            grabed, img = cap.read()
            if grabed:
                iset.append(dict(img=img,
                            fn=cap.get(cv.CV_CAP_PROP_POS_FRAMES),
                            ms=cap.get(cv.CV_CAP_PROP_POS_MSEC)))
                if len(iset) > size:
                    iset.popleft()
                yield(iset)
            i += 1

    def get_frames(self, ids=[], gray=False):
        self.__preload_cap()
        cap = self.cap["engine"]
        for fid in ids:
            cap.set(cv.CV_CAP_PROP_POS_FRAMES, fid)
            grabed, img = cap.read()
            if not grabed:
                continue
            if gray:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # idx = cap.get(cv.CV_CAP_PROP_POS_FRAMES)
            yield(dict(img=img, idx=int(fid)))

    def get_frame(self, by='id', value=0):
        key = dict(time=cv.CV_CAP_PROP_POS_MSEC, id=cv.CV_CAP_PROP_POS_FRAMES)
        cap = self.cap['cap']
        cap.set(key[by], value)
        grabed, img = cap.read()
        return img[:, :, [2, 1, 0]]  # convert for matplotlib, bgr

    def diff_pre(self, start=0, end=-1, fence="mild"):
        """
        Make absdiff of 2 images, return an array of the value and timestamp
        in ms.

        Params
        ------
        fence: statistical term to describe outlier range,
            "mild" and "extreme", use number for custom value.
        """
        data = np.array([[0, 0]])
        for imgs in self.scoped_frames(start=start, end=end, size=2):
            iis = [img['img'] for img in imgs]
            cur = len(imgs) - 1
            pre = cur - 1
            dst = cv2.absdiff(iis[cur], iis[pre])
            data = np.append(data, [[dst.sum(), imgs[cur]['ms']]], 0)
        df = pd.DataFrame(data[1:], columns=['isum', 'ms'])
        iqt = dict(mild=1.5, extreme=3, custom=fence)
        fence = "custom" if type(fence) is int else fence
        iqr = (df.isum.quantile(.75) - df.isum.quantile(.5))*iqt[fence]
        return df[df.isum.gt(iqr)]

    def __invalid_str_attr(self, name):
        return (not hasattr(self, name)) or \
            (self.__dict__[name] is None) or (self.__dict__[name] == "")

    def _assert_valid_str(self, name):
        if self.__invalid_str_attr(name):
            info = "Attribute {} is invalid.".format(name)
            raise Exception("Invalid Attribute Error", info)

    def __duration(self, start=0, end=-1):
        frame = int(self.cap['frames'])
        if (end < 0 or end > frame):
            end = frame
        return start, end+1

    def __load_cap(self):
        cap = cv2.VideoCapture(self.stream_path)
        fps = cap.get(cv.CV_CAP_PROP_FPS)
        frs = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
        self.cap = dict(engine=cap, fps=fps, frames=frs, seconds=frs/fps)
        self.cap_loaded = True

    def __reload_cap(self):
        self._assert_valid_str("stream_path")
        self.__load_cap()

    def __preload_cap(self):
        if not self.cap_loaded:
            self.__reload_cap()

    def __regulate_q(self, q, qsize, data):
        q.append(data)
        if len(q) > qsize:
            q.popleft()
        return q

    def frame_set(self, start=0, end=-1, qsize=2):
        """
        scoped_frame() improved
        """
        self.__preload_cap()
        dur = self.__duration(start, end)
        cap = self.cap['engine']
        iset = collections.deque([])
        ms_flag = cv.CV_CAP_PROP_POS_MSEC
        for ci in range(*dur):
            cap.set(cv.CV_CAP_PROP_POS_FRAMES, ci)
            grabed, img = cap.read()
            if grabed:
                data = dict(img=img, fn=ci, ms=cap.get(ms_flag))
                iset = self.__regulate_q(iset, qsize, data)
                if len(iset) < qsize:
                    continue
                yield(iset)
