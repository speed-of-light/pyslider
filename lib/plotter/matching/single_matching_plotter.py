import numpy as np
import cv2
from ... import Dataset
from ...exp.tools.video import Video
from ...exp.tools.slider import Slider
from ...plotter.base import Plotter


class SingleMatchingPlotter(Plotter, Dataset):
    def __init__(self, root, name, data, fid=-1, sid=-1):
        """
        Plot with single matched pairs (frame v.s. slide)
        data: dict contained needed dataframe within columns
        """
        Dataset.__init__(self, root, name)
        Plotter.__init__(self)
        self.fid = fid
        self.sid = sid
        self.data = data
        self.__load_colors()

    def __load_colors(self):
        cs = [(255, 24, 122), (249, 252, 157), (255, 232, 18),
              (3, 171, 85), (21, 159, 215), (217, 178, 255),
              (240, 250, 185), (200, 230, 155), (200, 200, 200)]
        self.rcolors = []
        for cc in cs:
            white = np.array((255, 255, 255))
            self.rcolors.append(white - np.array(cc))
        self.colors = cs

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

    def get_view(self):
        simg = self.__slide_image()
        fimg = self.__frame_image()
        view = self.__stiched_view(simg, fimg)
        return view

    def __get_mask(self, good, key):
        mask = [True] * len(good)
        fmap = dict(filtered=0, keep=1)
        if len(key) > 0:
            mask = (good.keep == fmap[key])
        return mask

    def __get_color(self, key, roi=0):
        loi = roi % len(self.colors)
        color = self.colors[loi]
        cmap = dict(filtered=self.colors[loi],
                    keep=self.rcolors[loi])
        if len(key) > 0:
            color = cmap[key]
        return color

    def __mpair_on_view(self, view, good, key='', roi=0):
        color = self.__get_color(key, roi+5)
        mask = self.__get_mask(good, key)
        view = self.__add_pos(view, good, mask, color)
        return view

    def __lines_on_view(self, view, good, key='', roi=0):
        y = 1
        qsize = self.data['qsize']
        color = self.__get_color(key, roi)
        mask = self.__get_mask(good, key)
        view = self.__add_lines(view, good, mask, qsize[y], color)
        return view

    def __roi_items(self, item, view, good):
        for rv, fg in good.groupby('roi'):
            view = self.__all_items(item, view, fg, int(rv))
        return view

    def __all_items(self, item, view, good, roi=0):
        key, ktype = item.split("_")
        if ktype == 'lines':
            view = self.__lines_on_view(view, good, key, roi)
        elif ktype == 'position':
            view = self.__mpair_on_view(view, good, key, roi)
        return view

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

    def matched_item(self, item, view, roi=False):
        """
        view: stiched images from frame and slides
        item: should be form as `filtered_lines`, `keep_position`, etc...
        Return image array
        """
        good = self.data['matches']
        if roi:
            view = self.__roi_items(item, view, good)
        else:
            view = self.__all_items(item, view, good)
        return view

    def hash_grid(self, view, hashes):
        """
        hashes example (origin at top left):
            [(500, 150),(200, 150),(200, 350), (500,350)]
        """
        simg = self.__slide_image()
        view = self.__add_hash(view, hashes, simg.shape)
        return view

    def layering(self, names=[], homo=None, hashes=None, roi=False):
        """
        Return image rendered with input ordered name layers
        Currently supported:
            `lines`, `homography`, `position`, `grid`
        """
        view = self.__get_view()
        for nn in names:
            sn = nn.split("_")
            if sn[1] in ['lines', 'position']:
                view = self.matched_item(nn, view, roi)
            if sn[1] == 'homo':
                view = self.homography(homo, view)
            if sn[1] == 'hash':
                view = self.hash_grid(view, hashes)
        return view
