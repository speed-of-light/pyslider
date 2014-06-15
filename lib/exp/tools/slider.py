import cv2
from ..summary import Summary
from pdf_reader import PdfReader


class Slider(object):
    """
    A helper to get slide information
    """
    def __init__(self, root="", name=""):
        self.root = root
        self.name = name

    def _blank_slide(self):
        sp = self.slides_path()
        img = cv2.imread("{}/{:03d}.jpg".format(sp, 1))
        img[:] = (255, 255, 255)  # fill white
        # red cross
        red = (0, 0, 255)
        line_width = int(0.1*img.shape[0])
        topL = (0, 0)
        botR = (img.shape[1], img.shape[0])
        topR = (0, img.shape[0])
        botL = (img.shape[1], 0)
        cv2.line(img, topL, botR, red, line_width)
        cv2.line(img, topR, botL, red, line_width)
        return img

    def _is_valid_sid(self, index, count):
        return (index > 0 and index < count+1)

    def _img_path(self, root, idx):
        return "{}/{:03d}.jpg".format(root, idx)

    def slide_pages(self):
        ps = Slider(self.root, self.name)
        return ps.pages()

    def slides_path(self, size='mid'):
        ps = PdfReader(self.root, self.name)
        return ps.slides_path(size)

    def get_slides(self, ids=[], gray=False, resize=None):
        """
        Get slide images collection
        """
        sp = self.slides_path(size='big')
        su = Summary()
        sin = su.info(self.root, self.name).iloc[0]
        if ids is None:
            ids = range(1, sin.n_slides+1)
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        for si in ids:
            sp = self._img_path(sp, si)
            if self._is_valid_sid(si, sin.n_slides):
                if gray:
                    img = cv2.imread(sp, cv2.COLOR_GRAY2BGR)
                else:
                    img = cv2.imread(sp)
            else:
                img = self._blank_slide()
                img = img[0] if gray else img
            if resize is not None:
                img = cv2.resize(img, resize)
            yield(dict(img=img, idx=si))

    def get_slide(self, index=1, resize=None):
        su = Summary()
        sin = su.info(self.root, self.name).iloc[0]
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        if self._is_valid_sid(index, sin.n_slides):
            spb = self.slides_path('big')
            img = cv2.imread(self._img_path(spb, index))
        else:
            img = self._blank_slide()
        if resize is not None:
            img = cv2.resize(img, resize)
        return img[:, :, [2, 1, 0]]  # convert for matplotlib
