import pandas as pd
import matplotlib.gridspec as gs
class HandyPlot:
  """
  Author: speed-of-light
  Purpose: show plot easily
  """

  @staticmethod
  def table( fig, img_list, title_list=None, row=2, col=2):
    """Print tablized image list
    Usage:
      fig = HandyPlot.table( plt.figure( figsize=(15, 12)), iml, 4, 4)
      fig.show()
    """
    b = row*col
    for i, img in enumerate(img_list, 1):
      ax = fig.add_subplot(row, col, i)
      title = "img_{}".format(i) if title_list is None else title_list[i-1]
      ax.set_title(title)
      ax.imshow(img)
      if i >= b: break
    return fig

  @staticmethod
  def match_compare(fig, vid_in, sli_in):
    """
    Usage:
      fig = HandyPlot.amtch_compare( plt.figure( figsize=(14, 4)), vid_data,
      sli_data)
      fig.show()
    """
    gsa = gs.GridSpec( 1, 10)
    gsa.update(left=0.01, right=0.99, hspace=0.25, wspace=.3)
    ax1 = fig.add_subplot(gsa[:, :-3], title="Input video")
    ax2 = fig.add_subplot(gsa[:, -3:], title="Self Compare")
    pax = ax1.matshow(vid_in)
    fig.colorbar(pax, ax=ax1)
    cax = ax2.matshow(sli_in)
    fig.colorbar(cax, ax=ax2)
    return fig

class HandyStat:
  """
  Author: speed-of-light
  Purpose: Statistical operations for image processing result
  """

  @staticmethod
  def posible_kf(afr=None, thres=0):
    """Return filtered slides
    By selecting the difference of slide with max key points count and mean key points count
    Sort and reorder
    Params:
      afr: All frame computed features result
      thres: filter threshold
    Returns:
      A dataframe contained timestamp(ms), diff value(val), slide id(sid)
      information
    Usage: run this twice...
      first = posible_kf(0) #generate diff values
      second = posible_kf(first.quantile(1-len(slides)*(torance)/1.0*len(first)).val)
    """
    gc = []
    gv = []
    gi = []
    for kc in afr.columns:
      kv = afr[kc].max() - afr[kc].quantile(.5)
      if kv >= thres:
        gc.append(int(kc[3:]))
        gv.append(kv)
        gi.append(afr[kc].idxmax())
    ret = pd.DataFrame()
    ret['ms'] = pd.Series(gc)
    ret['val'] = pd.Series(gv)
    ret['sid'] = pd.Series(gi)
    return ret

  @staticmethod
  def find_conseq(ary=[]):
    """Iterator for looping input array and find out consequtive flags.
    Params:
      ary: Integer array
    Returns:
      yield: start and end flags
    Example:
      for start, end in find_conseq([1,2,3,7,12,13,14]):
        print start, end
      >>> 1,3
      >>> 7,7
      >>> 12,14
    """
    start = end = ary[0]
    for iv in ary[1:]:
      if iv - end == 1:
        end = iv
      else:
        yield(start, end)
        start = end = iv
    if len(ary) > 0: yield(start, end)

  @staticmethod
  def time_delta(ms=0):
    """Format input milliseconds to hh:mm:ss with padding zeros
    """
    ts = ms/1000
    hours, remainder = divmod(int(ts), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

  @staticmethod
  def make_gnd(gt):
    """ Create single entry slide index
    :gt: dataframe that second column with slide indexes
    """
    fa = []; hold=-1
    for zv in gt.values:
      gv = zv[1]
      if gv > 0 and gv != hold:
        hold = gv
        fa.append(zv[0])
    return gt[gt.frame.isin(fa)]

class HandyStore:
  """Handling HDFstore
  """

  @property
  def cmplv(self):
    return 5

  def put(self, df, key):
    return self.store.put( key, df, format='t', data_columns=True,
        complib='blosc', complevel=self.cmplv)
    ""

  def __init__(self, path):
    self.path = '{}.h5'.format(path)
    self.store = pd.HDFStore(self.path, format='t', data_columns=True,
        complib='blosc', complevel=self.cmplv)
    ""

  def save_df(self, df, key):
    if key is None: return False
    """
    format='t' for table hdf
    data_columns to support table query, ex: where
    complib to reduce disc usage and speed up
    complevel from 0 to 9
    """
    df.to_hdf(self.path, key, mode='a', format='t', data_columns=True,
        complib='blosc', complevel=self.cmplv)

  def load_df(self, key):
    """
    global:
      summary
    local:
      './data/[root]/[name]/data
      keys:
        prepare:
          vital_frame:
            navie
            fast_navie
            key_frame_shot
            surf
          color_equal:
            hist
            gamma
        feats:
          keypoints:
            fast
            surf
            sift
            brisk
          descs:
            sift
            surf
            orb
            freak
            fast
            color_hist
            text_region
            hough_rect
          descs_sr: # frame descs within slide region # refinement
            sift
            surf
            orb
            freak
            fast
            color_hist
            text_region
        matched_feats:
          compare_hist
            correlation
            chi_square
            intersection
            Bhattacharyya
          svm
          pca
          brute_force
          flann
          ransac
        refine:
          time_series
            dtw
            hmm
            mdp
            gsm
          region_seek
            ransac
            hough_rect
    """
    return pd.read_hdf(self.path, key, format='t')

class HandyFormatter:
  """ Quick common formatters for pandas
  :cnt_: content targeting formatter
  :xml_: markup targeting formatter
  :tex_: latex targeting formatter
  """
  def cnt_gnd_status(v):
    ss = { '-1' : "no_slide", '1'   : "full_slide",
     '2'   : "small_slide", '-99' : "missing_slide" }
    return ss[str(v)]

  def cnt_gnd_vid_status(v):
    vs = [ "zoom_in", "stay_fixed", "zoom_out", "pan_tilt",
    "slide_cut1", "slide_cut2", "slide_in", "stay_out",
    "slide_out"]
    return vs[v]
