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

    def __add_poly(self, bound, dx, on_img):
        rimg = on_img[:]
        dxa = np.array([[[dx, 0]]]*4)
        cv2.polylines(rimg, bound+dxa, True, (0, 255, 0), 3)
        return rimg

    def __filtered_goods(self, good, mask):
        lg = good[mask]
        f_ = [int(lg.ix[mi].qix) for mi in lg.index]
        t_ = [int(lg.ix[mi].tix) for mi in lg.index]
        return zip(f_, t_)

    def __add_lines(self, view, good, mask, dx,
                    color=(100, 100, 255)):
        for fi, ti in self.__filtered_goods(good, mask):
            spt = self.data['sif']['kps'][fi].pt
            fpt = self.data['vif']['kps'][ti].pt
            smp = (int(spt[0]), int(spt[1]))
            fmp = (int(fpt[0] + dx), int(fpt[1]))
            cv2.line(view, smp, fmp, color, thickness=2)
        return view

    def __add_pos(self, view, good, mask, color=(100, 100, 255)):
        for fi, ti in self.__filtered_goods(good, mask):
            spt = self.data['sif']['kps'][fi].pt
            smp = (int(spt[0]), int(spt[1]))
            cv2.putText(view, "{},{}".format(fi, ti), smp,
                        cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
        return view

    def __cross_on_point(self, view, point, bound, color=(20, 230, 20)):
        x = 0
        y = 1
        cv2.line(view, (point[x], 0), (point[x], bound[0]), color, thickness=2)
        cv2.line(view, (0, point[y]), (bound[1], point[y]), color, thickness=2)

    def __add_hash(self, view, hash_, bound):
        """
        view: input image
        hash: four cross points of a hash (Quadrant rule)
        dx: delta x for left of the hash
        bound: max value of x and y
        """
        self.__cross_on_point(view, hash_[0], bound)
        self.__cross_on_point(view, hash_[2], bound)
        return view

    def __get_view(self):
        simg = self.__slide_image()
        fimg = self.__frame_image()
        view = self.__stiched_view(simg, fimg)
        return view

    def __get_mask(self, good, key):
        mask = None
        fmap = dict(filtered=0, keep=1)
        if len(key) > 0:
            mask = (good.keep == fmap[key])
        return mask

    def __get_color(self, key):
        color = (0, 200, 100)
        cmap = dict(filtered=(240, 160, 250),
                    keep=(100, 120, 230))
        if len(key) > 0:
            color = cmap[key]
        return color

    def _hash_from_roi(self, rois):
        """
        Development use:
            Plot only on simg
        """
        simg = self.__slide_image()
        for roi in rois:
            simg = self.__add_poly(roi, 0, simg)
        return simg

    def homography(self, homo, view=None):
        simg = self.__slide_image()
        fimg = self.__frame_image()
        if view is None:
            view = self.__stiched_view(simg, fimg)
        bound = self.__get_homo_bound(simg, fimg, homo)
        return self.__add_poly(bound, simg.shape[1], view)

    def matched_item(self, item, view):
        """
        view: stiched images from frame and slides
        item: should be form as `filtered_lines`, `keep_position`, etc...
        Return image array
        """
        simg = self.__slide_image()
        good = self.data['matches']
        si = item.split("_")
        mask = self.__get_mask(good, si[0])
        color = self.__get_color(si[0])
        if si[1] == 'lines':
            view = self.__add_lines(view, good, mask,
                                    simg.shape[1], color=color)
        if si[1] == 'position':
            view = self.__add_pos(view, good, mask, (0, 235, 20))
        return view

    def hash_grid(self, view, hashes):
        """
        hashes example (origin at top left):
            [(500, 150),(200, 150),(200, 350), (500,350)]
        """
        simg = self.__slide_image()
        view = self.__add_hash(view, hashes, simg.shape)
        return view

    def layering(self, names=[], homo=None, hashes=None):
        """
        Return image rendered with input ordered name layers
        Currently supported:
            `lines`, `homography`, `position`, `grid`
        """
        view = self.__get_view()
        for nn in names:
            sn = nn.split("_")
            if sn[1] in ['lines', 'position']:
                view = self.matched_item(nn, view)
            if sn[1] == 'homo':
                view = self.homography(homo, view)
            if sn[1] == 'hash':
                view = self.hash_grid(view, hashes)
        return view
