import numpy as np
import pandas as pd
import collections
import glob
import cv2
import cv


class Video(object):
    """
    Author: speed-of-light
    Purpose: Operations on video frames
    """
    @property
    def cap(self):
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

    def __init__(self, root, name):
        vid = glob.glob("./data/{}/{}/video.*".format(root, name))[0]
        self.stream_path = vid

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
        cap = self.cap['cap']
        for fid in ids:
            cap.set(cv.CV_CAP_PROP_POS_FRAMES, fid)
            grabed, img = cap.read()
            if not grabed:
                continue
            if gray:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            yield(dict(img=img, idx=fid))

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
