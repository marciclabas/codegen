from typing import Iterable
import importlib
import pkgutil

def walk_modules(pkg: str) -> Iterable[tuple[str, Exception | None]]:
  """Walks all submodules of `pkg`s and tries to import them. Yiels `(submodule, Exception)` for each import that fails"""
  try:
    mod = importlib.import_module(pkg)
    yield pkg, None
  except Exception as e:
    yield pkg, e
    return
  if not hasattr(mod, '__path__'):
    return
  for _, name, _ in pkgutil.iter_modules(mod.__path__):
    full_name = f"{pkg}.{name}"
    yield from walk_modules(full_name)