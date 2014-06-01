import numpy as np
import cv2
from ...data import Video
from ...exp.summary import Slider
from ...plotter.base import Plotter


class SingleMatchingPlotter(Plotter):
    def __init__(self, root, name, data, fid=-1, sid=-1):
        """
        data: dict contained needed dataframe within columns
        """
        Plotter.__init__(self, root, name, data)
        self.fid = fid
        self.sid = sid

    def set_matched_pair(self, fid=None, sid=None):
        """
        Interface to update current matched target
        """
        if fid is not None:
            self.fid = fid
        if sid is not None:
            self.sid = sid

    def set_data(self, data):
        """
        Interface to update dataframe
        """
        self.df = data

    def __frame_image(self, gray=False):
        """
        Returned a dict with keys: 'img', 'fid'
        """
        vv = Video(self.root, self.name)
        fi = vv.get_frames([self.fid], gray=gray).next()
        return fi['img']

    def __slide_image(self, gray=False):
        """
        Returned a dict with keys: 'img', 'fid'
        """
        ss = Slider(self.root, self.name)
        si = ss.get_slides([self.sid], gray=gray, resize=True).next()
        return si['img']

    def __stiched_view(self, left, right):
        """
        Generate stiched image
        """
        h1, w1 = left.shape[:2]
        h2, w2 = right.shape[:2]
        view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
        view[:h1, :w1] = left
        view[:h2, w1:] = right
        return view

    def __get_homo_bound(self, simg, fimg, homo):
        """
        Return bound(x, y):
            (top left), (bottom left), (bottom right), (top, right)
        """
        h, w, z = simg.shape
        pos = [[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
        bnd = np.float32(pos).reshape(-1, 1, 2)
        bound = cv2.perspectiveTransform(bnd, homo)
        # rimg = fimg[:]
        # cv2.polylines(rimg, [np.int32(bound)], True, (0, 255, 0), 3)
        return [np.int32(bound)]

    def __add_homo(self, bound, dx, on_img):
        rimg = on_img[:]
        dxa = np.array([[[dx, 0]]]*4)
        cv2.polylines(rimg, bound+dxa, True, (0, 255, 0), 3)
        return rimg

    def __add_lines(self, view, from_, to_, dx):
        for fi, ti in zip(from_, to_):
            spt = self.data['sif']['kps'][fi].pt
            fpt = self.data['vif']['kps'][ti].pt
            smp = (int(spt[0]), int(spt[1]))
            fmp = (int(fpt[0] + dx), int(fpt[1]))
            color = (100, 100, 255)
            cv2.line(view, smp, fmp, color, thickness=2)
            # cv2.putText(view, "{},{}".format(six, fix), smp,
            #            cv2.FONT_HERSHEY_PLAIN, 1, (0, 230, 0), 2)
        return view

    def __get_view(self):
        simg = self.__slide_image()
        fimg = self.__frame_image()
        view = self.__stiched_view(simg, fimg)
        return view

    def homography(self, homo, view=None):
        simg = self.__slide_image()
        fimg = self.__frame_image()
        if view is None:
            view = self.__stiched_view(simg, fimg)
        bound = self.__get_homo_bound(simg, fimg, homo)
        return self.__add_homo(bound, simg.shape[1], view)

    def matched_lines(self, view):
        """
        Return image array
        """
        simg = self.__slide_image()
        good = self.data['matches']
        flist = [int(good.ix[mi].qix) for mi in good.index]
        tlist = [int(good.ix[mi].tix) for mi in good.index]
        view = self.__add_lines(view, flist, tlist, simg.shape[1])
        return view

    def layering(self, homo, names=[]):
        """
        Return image rendered with input ordered name layers
        Currently supported:
            `lines`, `homography`, `position`, `grid`
        """
        view = self.__get_view()
        for nn in names:
            if nn is 'lines':
                view = self.matched_lines(view)
            if nn is 'homo':
                view = self.homography(homo, view)
        return view
