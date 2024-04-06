# Quicktype Ts

> Generate typescript types from pydantic models (or JSON schemas) using Quicktype


## Usage

Make sure you have `quicktype` installed:
  
```bash
npm -g i quicktype
```

```python
from pydantic import BaseModel, ConfigDict
from quicktype_ts import pydantic2typescript

class User(BaseModel):
  model_config = ConfigDict(extra='forbid')
  name: str
  age: int
  friends: list['User']

print(pydantic2typescript(User))
# export type User = {
#     age:     number;
#     friends: User[];
#     name:    string;
# }
```