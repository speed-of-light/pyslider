# Matching

## Synopsis

The core routine to get matched results

## Base Methods

- `Prepare` get filtered `diff_next/size_30` frames
- `Reducer` get reduced frames
- `Featx` get `SIFT_SIFT` keypoints
- `Matchx` get `BruteForce` matched pairs
- `DecisionMaker` get guessed `fid-sid` pairs
- `Evaluator` get result `precision`, `recall`, `fmeasure`, `accuracy`

## TODOs

`Matchx.Ransac` to make 1st order improve
`Matchx.Sloper` to make compare with `Ransac`
`Matchx.Second` to make 2nd order imporve
`Dtw` to do time wrap possibility check

# API

[API Reference](http://nbviewer.ipython.org/github/speed-of-light/pyslider/blob/master/docs/nb/matching_base.ipynb)
