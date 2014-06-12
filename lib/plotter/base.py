import matplotlib as mpl
import matplotlib.cm as mcm
from pylab import imread
from matplotlib.offsetbox import OffsetImage as ofb
from matplotlib.offsetbox import AnnotationBbox as abb


class Plotter(object):
    """
    Plotter base
    """
    def __init__(self, cmap=mcm.Paired):
        self.cmap = cmap
        self.seg_height = 10
        self.img_base = None
        #self.markers = [',', '+', '-', '.', 'o', '*', 'x']

    def markers(self):
        return ['o', '+', 'x', '*', '1', '2', '4', '8', 'D', 'd', 'h']

    def chunks(self, li, n):
        """ Yield successive n-sized chunks from li.  """
        for i in xrange(0, len(li), n):
            yield li[i:i+n]

    def image_box(self, path, loc, xyb, zoom=.1):
        img = imread(path)
        imb = ofb(img, zoom=zoom)
        ab = abb(imb, loc, xybox=xyb, pad=0,
                 xycoords="data", boxcoords="data")
        return ab

    def set_color_cycle(self, clist):
        """
        Set matplotlib build in color cycle by clist
        clist: should be a string list of color representation
            in `word` or `hex`
        example:
            # get color list example
            map(matplotlib.colors.rgb2hex, mpl.cm.Paired(range(0, 255, 27)))
        """
        mpl.rcParams['axes.color_cycle'] = clist


class SegLocator(object):
    def __init__(self, nth=0, height=10):
        """
        Get segment location information by given segment index and height
        """
        self.set_height(height)
        self.nth = nth

    def set_height(self, height):
        self.height = height
        self.__tag_at = height * 0.1
        self.__margin = height * 0.2
        self.__center = height * 0.5
        self.__content = height * 0.6

    def __brah_center(self, start, size):
        return start + size/2.0

    def __nth_base(self):
        """
        Return nth element of y-axis base position
        """
        return self.height * self.nth

    def yrange(self):
        """
        Return the range of y, start from (seg height)*si + content height,
            with height 6
        """
        return (self.__nth_base() + self.__margin,
                self.__content)

    def txt_pos(self, xinfo, tag_at=None):
        """
        xinfo: containing `start` and `size`, here use to get brah center
        """
        if tag_at is None:
            tag_at = self.__tag_at
        return (self.__brah_center(xinfo[0], xinfo[1]),
                self.__nth_base() + tag_at)

    def data_pos(self, xinfo):
        """
        xinfo: containing `start` and `size`, here use to get brah center
        """
        return (self.__brah_center(xinfo[0], xinfo[1]),
                self.__nth_base() + self.__center)
