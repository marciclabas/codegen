from typing import TypeVar
import subprocess
import json
from pydantic import BaseModel

def schema2typescript(json_schema: str, name: str) -> bytes:
  """Generate typescript code (returns code in raw bytes)"""
  args = [
    'quicktype', '-s', 'schema', '--lang', 'typescript', '--top-level', name,
    '--prefer-unions', '--prefer-types', '--prefer-const-values', '--just-types'
  ]
  return subprocess.check_output(args, input=json_schema.encode())

T = TypeVar('T', bound=BaseModel)
def pydantic2typescript(Model: type[T], name: str | None = None) -> bytes:
  """Generate typescript code (returns code in raw bytes)"""
  schema = json.dumps(Model.model_json_schema(mode='serialization'))
  return schema2typescript(schema, name or Model.__name__)