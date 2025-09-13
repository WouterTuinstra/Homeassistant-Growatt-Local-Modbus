#!/usr/bin/env bash
set -euo pipefail
echo "[postCreate] Starting setup..."

if [ -d /workspace ]; then
  cd /workspace || true
else
  echo "[postCreate] /workspace missing; using $(pwd)" >&2
fi

PY_BIN=""
echo "[postCreate] Searching for python interpreter..."
for c in python3.13 python3.12 python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY_BIN=$c; break; fi
done
if [ -z "$PY_BIN" ]; then
  echo "[postCreate] No python interpreter found" >&2
  exit 0
fi

if [ ! -d .venv ]; then
  echo "[postCreate] Creating venv using $PY_BIN";
  "$PY_BIN" -m venv .venv || { echo "[postCreate] venv creation failed" >&2; exit 0; }
else
  echo "[postCreate] Reusing existing venv";
fi
if [ ! -f .venv/bin/activate ]; then
  echo "[postCreate] Activate script missing; aborting" >&2; exit 0; fi
. .venv/bin/activate || { echo "[postCreate] Failed to activate venv" >&2; exit 0; }
echo "[postCreate] Python in venv: $(python -V 2>&1)"

echo "[postCreate] Upgrading pip tooling";
python -m pip install --upgrade pip wheel setuptools >/dev/null 2>&1 || true
if [ -f requirements_dev.txt ]; then
  echo "[postCreate] Installing requirements_dev.txt (may take a while)";
  pip install -r requirements_dev.txt || echo "[postCreate] requirements install reported errors" >&2
else
  echo "[postCreate] requirements_dev.txt not found";
fi
if [ -d external/growatt-rtu-broker ]; then
  echo "[postCreate] Installing broker editable";
  pip install -e external/growatt-rtu-broker || echo "[postCreate] broker install error" >&2
else
  echo "[postCreate] broker directory missing (optional)";
fi

echo "[postCreate] Done"
