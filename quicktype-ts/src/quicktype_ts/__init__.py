"""
### Quicktype Ts
> Generate typescript types from pydantic models (or JSON schemas) using Quicktype

#### Usage

- Make sure to install `quicktype` with `npm -g i quicktype`

```
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
"""
from .main import pydantic2typescript, schema2typescript