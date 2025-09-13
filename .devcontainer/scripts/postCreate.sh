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

create_or_recreate_venv() {
  rm -rf .venv || true
  echo "[postCreate] (Re)creating venv using $PY_BIN";
  "$PY_BIN" -m venv .venv || "$PY_BIN" -m ensurepip --upgrade || true
}

if [ ! -d .venv ]; then
  create_or_recreate_venv
else
  echo "[postCreate] Reusing existing venv";
fi

if [ ! -f .venv/bin/activate ]; then
  echo "[postCreate] Activate script missing; attempting recreate" >&2
  create_or_recreate_venv
fi

. .venv/bin/activate || { echo "[postCreate] Failed to activate venv" >&2; exit 0; }
echo "[postCreate] Python in venv: $(python -V 2>&1)"

# Detect broken pip (common on glibc mismatch) and repair
if [ ! -x .venv/bin/pip ]; then
  echo "[postCreate] pip not executable; repairing with ensurepip" >&2
  python -m ensurepip --upgrade || true
fi
python -m pip --version || { echo "[postCreate] pip still broken" >&2; }

echo "[postCreate] Upgrading pip tooling";
python -m pip install --upgrade pip wheel setuptools || echo "[postCreate] pip tooling upgrade had issues" >&2
if [ -f requirements_dev.txt ]; then
  echo "[postCreate] Installing requirements_dev.txt (may take a while)";
  python -m pip install -r requirements_dev.txt || echo "[postCreate] requirements install reported errors" >&2
else
  echo "[postCreate] requirements_dev.txt not found";
fi
if [ -d external/growatt-rtu-broker ]; then
  echo "[postCreate] Installing broker editable";
  python -m pip install -e external/growatt-rtu-broker || echo "[postCreate] broker install error" >&2
else
  echo "[postCreate] broker directory missing (optional)";
fi

echo "[postCreate] Done"
