"""
### Openapi Ts
> Generate typescript clients for OpenAPI (e.g. FastAPI) apps, using openapi-ts

#### Usage

- Make sure to install `openapi-ts` with `npm -g i @hey-api/openapi-ts`

```python
from fastapi import FastAPI
from pydantic import BaseModel
from openapi_ts import generate_client

# define your app
app = FastAPI(generate_unique_id_function=lambda route: route.name)

class User(BaseModel):
  name: str
  email: str

@app.get('/users')
def get_users(how_many: int | None = None) -> list[User]:
  ...

# generate client
generate_client(app.openapi(), 'path/to/client')
```
"""
from .main import generate_client