# Py Jaxtyping

> Pydantic support for Jaxtyping array annotations

## Usage
  
Instead of `Int[np.ndarray, 'B 256 64 3']`, do `PyArray[Int, int, 'B 256 64 3']`

You can use it with `jaxtyping` as normal, but also it will:
- Serialize to nested lists
- Validate the correct shape and datatypes from serialized lists

### Example
```
from pydantic import BaseModel, ConfigDict
from py_jaxtyping import PyArray
from jaxtyping import Int
import numpy as np

class Sample(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  img: PyArray[Int, int, "W H 3"]
  label: str

Sample.model_validate({
  'img': np.ones((256, 64, 3)),
  'label': 'car'
})
# checks out!


Sample.model_validate({
  'img': np.ones((256, 64, 1)),
  'label': 'car'
})
# fails: invalid dims :/
```