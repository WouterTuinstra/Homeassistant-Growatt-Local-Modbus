#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)

if ! command -v socat >/dev/null 2>&1; then
  echo "Error: socat is required to create pseudo-terminals" >&2
  exit 1
fi

TMP_LOG=$(mktemp)
SOCAT_PID=""
SIM_PID=""
cleanup() {
  local status=$?
  trap - EXIT INT TERM
  if [[ -n "${SIM_PID}" ]]; then
    kill "${SIM_PID}" 2>/dev/null || true
  fi
  if [[ -n "${SOCAT_PID}" ]]; then
    kill "${SOCAT_PID}" 2>/dev/null || true
  fi
  rm -f "${TMP_LOG}"
  exit ${status}
}
trap cleanup EXIT INT TERM

socat -d -d PTY,raw,echo=0 PTY,raw,echo=0 2>"${TMP_LOG}" &
SOCAT_PID=$!

# Wait for socat to report both PTY device paths
while [[ $(grep -c 'PTY is' "${TMP_LOG}") -lt 2 ]]; do
  if ! kill -0 "${SOCAT_PID}" 2>/dev/null; then
    cat "${TMP_LOG}" >&2 || true
    echo "Failed to create pseudo terminals" >&2
    exit 1
  fi
  sleep 0.1
done

mapfile -t PORTS < <(awk '/PTY is/ {print $NF}' "${TMP_LOG}")
if [[ ${#PORTS[@]} -lt 2 ]]; then
  echo "Unable to determine pseudo terminal paths" >&2
  exit 1
fi
SIM_PORT="${PORTS[0]}"
CLIENT_PORT="${PORTS[1]}"

echo "Simulator serial port: ${SIM_PORT}" >&2
echo "Client serial port: ${CLIENT_PORT}" >&2
# Print the client-facing port so callers can capture it easily
printf '%s\n' "${CLIENT_PORT}"

PYTHON_BIN=${PYTHON:-python}
"${PYTHON_BIN}" "${REPO_ROOT}/testing/modbus_simulator.py" --mode serial --serial-port "${SIM_PORT}" "$@" &
SIM_PID=$!

wait "${SIM_PID}"
