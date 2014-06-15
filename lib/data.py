from PyPDF2 import PdfFileReader
import shutil
# from wand.image import Image, Color
from pgmagick import Image
from PIL import Image as pimg


class PdfReader(object):
    """
    Author: speed-of-light
    Purpose: Operations on pdf files
    """
    def __init__(self, root="", name=""):
        """ Init data with project name and root dir
        root: base dir of pdf and video data
        """
        self.root = root
        self.name = name
        self.pages = None
        if os.path.isfile(self.pdf_path):
            pdf = PdfFileReader(self.pdf_path)
            self.pages = pdf.getNumPages()

    def slides_path(self, size="mid"):
        """The root of converted slide images
        """
        rt = self.root if self.root == "" else "{}/".format(self.root)
        return "./data/{1}{0}/slides/{2}".format(self.name, rt, size)

    @property
    def pdf_path(self):
        """The root of converted slide images
        """
        rt = self.root if self.root == "" else "{}/".format(self.root)
        return "./data/{1}{0}/{0}.pdf".format(self.name, rt)

    def png_jpg(self, path):
        png = "{}.png".format(path)
        jpg = "{}.jpg".format(path)
        pimg.open(png).convert('RGB').save(jpg)
        os.remove(png)

    def to_jpgs(self, size='mid', pages=None):
        """ Convert pdf to jpeg images
          pages: array for pages, None for extract all
        """
        dendic = dict(thumb=40, mid=100, big=150)
        density = dendic[size]
        pages = np.arange(0, self.pages, 1) if pages is None else pages
        if len(pages) < 1:
            return
        sp = self.slides_path(size)
        if os.path.exists(sp):
            shutil.rmtree(sp)
        os.makedirs(sp)
        img = Image()
        img.density("{}".format(density))
        for page in pages:
            if page > self.pages or page < 0:
                continue
            pdf = "{}[{}]".format(self.pdf_path, page)
            slid = "{}/{:03d}".format(sp, page)
            img.read(pdf)
            img.write("{}.jpg".format(slid))
        # break
        # self.png_jpg('test.png')
