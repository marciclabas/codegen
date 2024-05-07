mod quicktype-ts
mod openapi-ts
mod py-jaxtyping
mod templang
mod verify-import

VENV := ".venv"
PYTHON := ".venv/bin/python"

help:
  @just --list

init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt