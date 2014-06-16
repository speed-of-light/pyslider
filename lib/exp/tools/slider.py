import cv2
from ..summary import Summary
from pdf_reader import PdfReader


class Slider(PdfReader):
    """
    A helper to get slide information
    """
    def __init__(self, root="", name=""):
        PdfReader.__init__(self, root, name)

    def __blank_slide(self, gray=False):
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
        if gray:
            return img[0]
        else:
            return img

    def __is_valid_sid(self, index, count):
        return (index > 0 and index < count+1)

    def __img_path(self, idx):
        sp = self.slides_path(size='big')
        return "{}/{:03d}.jpg".format(sp, idx)

    def __info(self):
        su = Summary()
        sin = su.info(self.root, self.name)
        return sin

    def slide_pages(self):
        ps = PdfReader(self.root, self.name)
        return ps.pages()

    def slides_path(self, size='mid'):
        ps = PdfReader(self.root, self.name)
        return ps.slides_path(size)

    def __make_img(self, idx, itop, path, gray):
        if self.__is_valid_sid(idx, itop):
            if gray:
                img = cv2.imread(path, cv2.COLOR_GRAY2BGR)
            else:
                img = cv2.imread(path)
        else:
            img = self.__blank_slide(gray)
        return img

    def get_slides(self, ids=[], gray=False, resize=None):
        """
        Get slide images collection
        use img[:, :, [2, 1, 0]] to convert for matplotlib
        """
        sin = self.__info()
        if ids is None:
            ids = range(1, sin.n_slides+1)
        if resize is True:
            resize = (sin.v_width, sin.v_height)
        for si in ids:
            sp = self.__img_path(si)
            img = self.__make_img(si, sin.n_slides, sp, gray)
            if resize is not None:
                img = cv2.resize(img, resize)
            yield(dict(img=img, idx=si))
