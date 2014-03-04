import pandas as pd

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
