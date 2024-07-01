from typing import Mapping, TextIO
import os
from tempfile import mktemp
import json

def generate_client(
  openapi_schema: dict, package_path: str, *,
  args: Mapping[str, str] = {
    '--client': '@hey-api/client-fetch',
    '--services': '{ asClass: false }'
  },
  logstream: TextIO | None = None
):
  """Generate client for `openapi_schema` at `package_path`
  - `args` are passed to `openapi-ts`
  """
  if logstream:
    print('Generating client...', file=logstream)
  file = mktemp(prefix='openapi-', suffix='.json')
  with open(file, 'w') as f:
    json.dump(openapi_schema, f)

  os.makedirs(package_path, exist_ok=True)
  os.chdir(package_path)
  if not os.path.exists('package.json'):
    with open('package.json', 'w') as f:
      f.write('{}')

  str_args = ' '.join(f'{k} {v}' for k, v in args.items())
  os.system(f'npx @hey-api/openapi-ts -i {file} -o src/ {str_args}')

  # replace all ".gen'" with ".gen.js'" inside the generated files
  if logstream:
    print('Fixing generated files for NodeNext imports...', file=logstream)
  for root, _, files in os.walk('src'):
    for file in files:
      if file.endswith('.ts'):
        with open(os.path.join(root, file), 'r') as f:
          content = f.read()
        with open(os.path.join(root, file), 'w') as f:
          f.write(content.replace('.gen\'', '.gen.js\''))

  if logstream:
    print('Client generated!', file=logstream)