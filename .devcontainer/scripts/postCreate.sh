#!/usr/bin/env bash
set -euo pipefail

cd /workspace || cd "$PWD"

PY_BIN=""
for c in python3.13 python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY_BIN=$c; break; fi
done
if [ -z "$PY_BIN" ]; then
  echo "[postCreate] No python interpreter found" >&2
  exit 0
fi

if [ ! -d .venv ]; then
  echo "[postCreate] Creating venv using $PY_BIN";
  "$PY_BIN" -m venv .venv
fi
. .venv/bin/activate || { echo "[postCreate] Failed to activate venv" >&2; exit 0; }

python -m pip install --upgrade pip wheel setuptools >/dev/null 2>&1 || true
if [ -f requirements_dev.txt ]; then
  echo "[postCreate] Installing requirements_dev.txt";
  pip install -r requirements_dev.txt || true
fi
if [ -d external/growatt-rtu-broker ]; then
  echo "[postCreate] Installing broker editable";
  pip install -e external/growatt-rtu-broker || true
fi

echo "[postCreate] Done"
