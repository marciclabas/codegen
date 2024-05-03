from typing import Sequence, Literal, TypeAlias, Mapping

Context = Literal['template', 'loop']
Stack: TypeAlias = list[Context]

def drop_while(p, xs):
  for i, x in enumerate(xs):
    if not p(x):
      return xs[i:]
  return []

def parse(source_code: str, translations: Mapping[str, str | Sequence[str]], prefix: str = '#') -> str:
  """
  - `source_code`: source code to process
  - `translations`: stuff to replace in the source code
  - `prefix`: prefix for annotations, defaults to `#`

  ### Rules
  >> In what follows, `#` refers to the `prefix` argument: <<
  - `# BEGIN` and `# END` delimit a template
  - Lines starting with `# UNCOMMENT` are stripped to whatever proceeds the annotation
  - Lines ending with `# DELETE` are removed
  - `# LOOP VAR1 ... VARN` and `# END` delimit a loop:
    - `translations[VARi]` must be a sequence of strings
    - `LEN = len(translations[VAR1]) == ... == len(translations[VARN])`
    - The template inside the loop is substituted with translations[VARi][j] for each `j in range(LEN)`	
    - Nested loops are allowed
  """
  
  def _parse(lines: list[str], stack: Stack, translations: dict[str, str | Sequence[str]]) -> tuple[list[str], Stack]:
    if lines == []:
      return [], stack
    
    line, *rest = lines

    if line.strip().startswith(f'{prefix} BEGIN'):
      return _parse(rest, [*stack, 'template'], translations)
    
    elif stack == []:
      return _parse(rest, stack, translations)
    
    if line.strip().startswith(f'{prefix} END'):
      return [], stack[:-1]
    
    if f'{prefix} DELETE' in line:
      return _parse(rest, stack, translations)
    
    if line.strip().startswith(f'{prefix} LOOP'):
      variables = line.split(f'{prefix} LOOP')[1].strip().split(' ')
      try:
        values = { var: translations[var] for var in variables }
      except KeyError:
        raise ValueError(f"Missing translations for {[var for var in variables if var not in translations]}")
      
      loop_lines = []
      for i in range(max(len(values[var]) for var in variables)):
        nested_translations = translations | { var: values[var][i] for var in variables }
        lines, _ = _parse(rest, [*stack, 'loop'], nested_translations)
        loop_lines.extend(lines)

      skip_loop = drop_while(lambda x: not x.strip().startswith(f'{prefix} END'), rest)[1:]
      next_lines, next_stack = _parse(skip_loop, stack, translations)
      return [*loop_lines, *next_lines], next_stack
    
    output = line.strip('\n')
    if line.strip().startswith(f'{prefix} UNCOMMENT'):
      output = line.strip().split(f'{prefix} UNCOMMENT')[1].strip()

    for key, value in translations.items():
      if isinstance(value, str):
        output = output.replace(key, value)

    next_lines, next_stack = _parse(rest, stack, translations)
    return [output, *next_lines], next_stack

  lines = source_code.split('\n')
  processed, _ = _parse(lines, [], dict(translations))
  return '\n'.join(processed)