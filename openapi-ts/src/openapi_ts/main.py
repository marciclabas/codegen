from typing import Mapping, TextIO
import os
from tempfile import mktemp
import json

def generate_client(
  openapi_schema: dict, output_path: str, *,
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

  str_args = ' '.join(f'{k} {v}' for k, v in args.items())
  cmd = f'npx @hey-api/openapi-ts -i {file} -o {output_path} {str_args}'
  if logstream:
    print(f'Running: {cmd}', file=logstream)
  os.system(cmd)

  # replace all ".gen'" with ".gen.js'" inside the generated files
  if logstream:
    print('Fixing generated files for NodeNext imports...', file=logstream)
  for root, _, files in os.walk(output_path):
    for file in files:
      if file.endswith('.ts'):
        with open(os.path.join(root, file), 'r') as f:
          content = f.read()
        with open(os.path.join(root, file), 'w') as f:
          f.write(content.replace('.gen\'', '.gen.js\''))

  if logstream:
    print('Client generated!', file=logstream)