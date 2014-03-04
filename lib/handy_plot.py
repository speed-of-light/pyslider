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
