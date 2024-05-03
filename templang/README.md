# templang

> A simple annotation-based language to generate code from templates

## Templates

Templates are just source files with annotations. For example:

```python
# BEGIN
from typing import Literal

Rank = Literal[
  # LOOP RANK
  'RANK',
  #END
]

CLEARANCE_LEVEL = int # DELETE (just to make mypy happy)
# LOOP RANK CLEARANCE_LEVEL
class RANK:
  clearance_level: CLEARANCE_LEVEL

# END


# END
```

## Template Parsing

```python
from templang import parse
with open('ranks.py') as f:
  source = f.read()

code = parse(source, translations={
  'RANK': ['Captain', 'Lieutenant', 'Sergeant'],
  'CLEARANCE_LEVEL': ['1', '2', '3']
})

print(code)

# from typing import Literal
# 
# Rank = Literal[
#   'Captain',
#   'Lieutenant',
#   'Sergeant',
# ]
# 
# class Captain:
#   clearance_level: 1
# 
# class Lieutenant:
#   clearance_level: 2
# 
# class Sergeant:
#   clearance_level: 3
```

## Rules

Now, that's most of what you need to now. But, to be precise, here are the rules:

- `# BEGIN` and `# END` delimit a template
- Lines starting with `# UNCOMMENT` are stripped to whatever proceeds the annotation
- Lines ending with `# DELETE` are removed
- `translations: Mapping[str, str | Sequence[str]]` is the dictionary of translations:
  - If `value = translations[key]` is a string, all instances of `key` are replaced by `value`
  - If `value = translations[key]` is a sequence of strings, `key` will be allowed in a `# LOOP` declaration
  - The order of translations is not guaranteed. So, keys substrings of other keys will probably yield inentended results
- `# LOOP VAR1 ... VARN` and `# END` delimit a loop:
  - `translations[VARi]` must be a sequence of strings
  - `LEN = len(translations[VAR1]) == ... == len(translations[VARN])`
  - The template inside the loop is substituted with `translations[VARi][j]` for each `j in range(LEN)`	
  - Nested loops are allowed

- Oh, and actually, `#` can be replaced by any custom string (e.g. `//`)