# Features

- Synopsis: Class to collecting feature data from `frames` and `slides`.

## Structure

- root: `stores/featx`
  + algo formed store filename
    * `keys`
    * `f_number`
    * `s_number`
    * `stats`
    * extends to save filtered, adjusted results

## Examples

### Featx

```python
from lib.exp.featx import Featx
ft = Featx(root, name)
# Get all slide feats
ft.get_slide_feats()
# Get all video frames feats
ft.get_frame_feats()
```

