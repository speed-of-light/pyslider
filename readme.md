# Release Notes

* Milestone: **0.3.0** 2014-04-10
  - have finish Feats class
  - have basic latex generator for diagrams and tables for Feats class
  - have informatic data summary class

* Milestone: **0.2.0** 2014-04-05
  - have finish Prepare class
  - have basic latex generator for diagrams and tables for Prepare class

- `0.1.5`: 2014-03-26 Wed 02:53 PM
  - mock up needed classes
  - create a base framework for collecting data

  global: './data/store.h5'
    summary
  local: './data/[root]/[name]/store/[data].h5'
    ======================================================================
    | prepare          | feats         | matched_feats  | refinement     |
    ----------------------------------------------------------------------
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
    ======================================================================


- 0.1.0: 2014-03-05 Wed 11:21 AM
 - release for backup
 - mainly build up seperated functions

