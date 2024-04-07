from typing import Annotated, Any, Unpack, Literal, TypedDict, TypeVar
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema
from pydantic_core import CoreSchema
from pydantic_core.core_schema import no_info_after_validator_function
import numpy as np

class SchemaKeys(TypedDict):
  array: str
  dtype: str
  items: str
  minItems: str
  maxItems: str

def array_schema(dims: list, **keys: Unpack[SchemaKeys]) -> dict[str, Any]:
  """Schema for a `len(dims)`-dimensional array
  - `dims[i]` can be
    - an integer: to denote a fixed shape
    - anything else: to denote a variable shape

  e.g. `dims=['N', 2, '5']`
  """
  match dims:
    case [dim] if str(dim).isdecimal():
      d = int(dim)
      return {
        'type': keys['array'], keys['items']: array_schema([], **keys),
        keys['minItems']: d, keys['maxItems']: d
      }
    case [dim, *ds] if str(dim).isdecimal():
      d = int(dim)
      return {
        'type': keys['array'], keys['items']: array_schema(ds, **keys),
        keys['minItems']: d, keys['maxItems']: d
      }
    case [dim, *ds]:
      return {
        'type': keys['array'], keys['items']: array_schema(ds, **keys),
      }
    case _:
      return { 'type': keys['dtype'] }


def json_schema(dims: list) -> dict[str, Any]:
  return array_schema(
    dims, array='array', dtype='number', items='items',
    minItems='minItems', maxItems='maxItems'
  )

def core_schema(dims: list, dtype: Literal['int', 'float', 'bool'] = 'int') -> CoreSchema:
  return array_schema(
    dims, array='list', dtype=dtype, items='items_schema',
    minItems='min_length', maxItems='max_length'
  ) # type: ignore


class PyArray:
  """A `jaxtyping` array that can be used with pydantic
  
  Instead of:
  >>> Int[np.ndarray, 'B 256 64 3']
  do:
  >>> PyArray[Int, 'B 256 64 3']

  You can use it with `jaxtyping` as normal, but also

  ```
  class WithArray(BaseModel):
    arr: PyArray[Int, 'B 256 64 3']
  ```

  And it will:
  - Serialize to nested lists
  - Validate the correct shape and datatypes from serialized lists
  """
  def __class_getitem__(cls, params: tuple[type, str]):
    DType, dims = params
    return Annotated[
      DType[np.ndarray, dims],
      AfterValidator(np.array),
      PlainSerializer(lambda arr: arr.tolist()),
      WithJsonSchema(json_schema(dims.split(' ')))
    ]