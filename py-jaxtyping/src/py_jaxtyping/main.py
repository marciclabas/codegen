from pydantic_core.core_schema import no_info_after_validator_function
import numpy as np
from .schemas import core_schema

def str_type(DType: type[int] | type[float] | type[bool]):
  if DType is int:
    return 'int'
  if DType is float:
    return 'float'
  if DType is int:
    return 'bool'

class PyArray:
  """A `jaxtyping` array that can be used with pydantic
  
  Instead of:
  >>> Int[np.ndarray, 'B 256 64 3']
  do:
  >>> PyArray[Int, 'B 256 64 3']

  You can use it with `jaxtyping` as normal, but also

  ```
  class WithArray(BaseModel):
    arr: PyArray[Int, int, 'B 256 64 3']
  ```

  And it will:
  - Serialize to nested lists
  - Validate the correct shape and datatypes from serialized lists
  """
  def __class_getitem__(cls, params: tuple[type, type[int] | type[bool] | type[float], str]):
    DType, dtype, dims = params
    Type = DType[np.ndarray, dims]
    class Cls(Type):

      __name__ = f'Py{DType.__name__}Array[{dims}]'
      __qualname__ = __name__

      @classmethod
      def __get_pydantic_core_schema__(cls, *_):
        def validate(xs: list):
          arr = np.array(xs)
          if not isinstance(arr, Type):
            raise ValueError('Invalid array')
          return arr

        return no_info_after_validator_function(validate, core_schema(dims.split(' '), str_type(dtype))) # type: ignore

    return Cls