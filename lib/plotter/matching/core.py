import numpy as np
from lib import Dataset
from lib.exp.tools.video import Video
from lib.exp.tools.slider import Slider
from lib.plotter.base import Plotter


class MatchingPlotterBase(Plotter, Dataset):
    def __init__(self, root, name, data=None, sid=-1, fid=-1):
        """
        MatchingPlotter core functions
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

    def __frame_image(self, gray=False, show_pos=False):
        """
        show_pos: will stdout next frame position of aquired frame id
            ,for helping debug.
        Returned a dict with keys: 'img', 'fid'
        """
        vv = Video(self.root, self.name)
        fi = vv.get_frames([self.fid], gray=gray).next()
        if show_pos:
            print fi["idx"]
        return fi["img"]

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

    def get_view(self, show_pos=False):
        simg = self.__slide_image()
        fimg = self.__frame_image(show_pos=show_pos)
        view = self.__stiched_view(simg, fimg)
        return view

    def set_matched_pair(self, sid=None, fid=None):
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
