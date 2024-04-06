mod quicktype-ts
mod openapi-ts

VENV := ".venv"
PYTHON := ".venv/bin/python"

init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt