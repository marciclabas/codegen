import os
from tempfile import mktemp
import json

def generate_client(openapi_schema: dict, package_path: str, *, args: str = ''):
  """Generate client for `openapi_schema` at `package_path`
  - `args` are passed to `openapi-ts` (by default, only `-i` and `-o` are passed)
  """
  file = mktemp(prefix='openapi-', suffix='.json')
  with open(file, 'w') as f:
    json.dump(openapi_schema, f)

  os.makedirs(package_path, exist_ok=True)
  os.chdir(package_path)
  if not os.path.exists('package.json'):
    with open('package.json', 'w') as f:
      f.write('{}')
  os.system(f'openapi-ts -i {file} -o src/ {args}')