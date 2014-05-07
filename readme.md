# Release Notes

* Milestone: **0.5.0** 2014-04-30
  - support latex generator for diagrams and tables for Prepare class
  - basic main flow

* Milestone: **0.4.0** 2014-04-29
  - have basic latex generator for diagrams and tables for Feats class

* Milestone: **0.3.5** 2014-04-25
  - More informatic data summary class

- `0.3.5`: 2014-05-07 Wed 10:42 PM
  - Add simple matching flow with groundtruth check

- `0.3.0`: 2014-04-28 Mon 06:29 AM
  - Seperate exp into other submodules
  - Add `set_match` to `Matcher` class

- `0.2.3`: 2014-04-26 Sat 09:33 PM
  - Add reduce frame flow to `Prepare`
  - Add `notify` to `ExpCommon`

- `0.2.2`: 2014-04-24 Thu 11:16 PM
  - handling long term process error
  - make common class tool flexible

- `0.2.1`: 2014-04-24 Thu 07:02 PM
  - deploy for computing slides feats

- `0.2.0`: 2014-04-23
  - Add `ExpCommon` to support common operations
  - Develope `GroundTruth` class
  - `Feats` with `o_slides()`, `detect_with()` functions
  - `Feats` with compute all defaults method

- `0.1.6`: 2014-03-28 Fri 06:09 PM
  - add diff with average frames
  - make diff function more flexible for accept params
  - Add profiler for time and memory

- `0.1.5`: 2014-03-26 Wed 02:53 PM
  - mock up needed classes
  - create a base framework for collecting data

  global: './data/store.h5'
    summary
  local: './data/[root]/[name]/store/[data].h5'

| prepare          | feats         | matched_feats  | refinement     |
|-----------------:|:-------------:|:--------------:|:---------------|
| vital_frame:     | keypoints:    | compare_hist   | refine:        |
|   `diff_next`    |   fast        |   correlation  |   time_series  |
|   diff_bkg       |   surf        |   chi_square   |     dtw        |
|   key_frame_shot |   sift        |   intersection |     hmm        |
|   surf           |   brisk       |   Bhattacharyy |     mdp        |
| color_equal:     | descs:        | svm            |     gsm        |
|   hist           |   sift        | pca            |   region_seek  |
|   gamma          |   surf        | brute_force    |     ransac     |
|                  |   orb         | flann          |     hough_rect |
|                  |   freak       | ransac         |                |
|                  |   fast        |                |                |
|                  |   color_hist  |                |                |
|                  |   text_region |                |                |                                                                                 a
|                  |   hough_rect  |                |                |


- 0.1.0: 2014-03-05 Wed 11:21 AM
 - release for backup
 - mainly build up seperated functions


# Misc

Modified tags in univ data set:
`coates`: `4289` to `4567` from `-1, -1, -1` to `1, 1, 1`
