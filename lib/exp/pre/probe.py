import cv2
from lib.exp.tools.preloader import Preloader
from lib.exp.tools.timer import ExpTimer


class Probe(Preloader):
    def __init__(self, root, name):
        """
        Probing video frames and do some computation
        """
        Preloader.__init__(self)
        self.set_rootname(root, name)

    def set_rootname(self, root, name):
        self.root = root
        self.name = name

    def __get_local_avgimg(self, imgs, ratio=0):
        mix = imgs[0]
        mix = cv2.addWeighted(mix, ratio, mix, 0, 0)
        for img in imgs[1:-1]:
            mix = cv2.addWeighted(mix, 1, img, ratio, 0)
        sumi = cv2.absdiff(imgs[-1], mix).sum()
        return sumi

    def diff_next(self, end=-1, qs=2):
        Preloader._preload(self, "video")
        ratio = 1.0/qs
        ret = []
        for imds in self.video.frame_set(start=0, end=end, qsize=qs):
            with ExpTimer(verbose=False) as t:
                imgs = [im["img"] for im in imds]
                sumi = self.__get_local_avgimg(imgs, ratio)
            data = dict(htime=t.msecs, ms=imds[-1]['ms'], diff=sumi, frame_id=imds[-1]['fn'])
            ret.append(data)
            yield imds[-1]['fn'], "OP time:", t.tstr()
        self.pdf = pd.DataFrame(ret)  # columns=['ms', 'frame_id', 'diff']
