# GroundTruth

## Synopsis:

Handling groundtruth data

## Manual add marks

```python
from lib.auto import Doer
do = Doer(root, name)
do.add_mark(fig, sid, fid, pre)
```

There are also `delete_mark`, `save_marks`

## Expected data

- `abs_pairs`: containing key pairs consisted by `fid`, `sid`, `slide type`,
`cam status`, both `fid`, and `sid` should larger than `0`.
- `rel_pairs`: containing only the unique `sid` within keep the order in
`abs_pairs`.
- `segments`: contains segmentation data.

## Collected datasets

- Datasets: `univ`, `wang`, `lab`

## Examples

### Manual add makrs

- Add marks by `doer`: [demo](http://nbviewer.ipython.org/github/speed-of-light/pyslider/blob/master/docs/nb/ground_truth/manual_mark.ipynb)

### Plot

- Plot even splited segments of ground truth: [demo](http://nbviewer.ipython.org/github/speed-of-light/pyslider/blob/master/docs/nb/ground_truth/GtSegments.ipynb)
- Plot slide-frame pairs from a single dataset: [demo](http://nbviewer.ipython.org/github/speed-of-light/pyslider/blob/master/docs/nb/ground_truth/GtDirectMatch.ipynb)
- Plot pairs from multiple dataset: [demo](http://nbviewer.ipython.org/github/speed-of-light/pyslider/blob/master/docs/nb/ground_truth/grouping_pairs.ipynb)
