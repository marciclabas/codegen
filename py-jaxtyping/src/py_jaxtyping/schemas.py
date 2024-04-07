from typing import Annotated, Any, Unpack, Literal, TypedDict, TypeVar
from pydantic_core import CoreSchema

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
    case [dim]:
      return {
        'type': keys['array'], keys['items']: array_schema([], **keys),
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