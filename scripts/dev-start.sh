#!/usr/bin/env bash
set -euo pipefail

ACTION=${1:-noop}
DEFAULT_BASE=/workspace
if [ -w /workspace ] || [ ! -e /workspace ]; then
  BASE=$DEFAULT_BASE
else
  BASE=$(pwd)
  echo "[dev-start] /workspace not writable; using $BASE" >&2
fi
VENVDIR=$BASE/.venv
HACONF=$BASE/ha_config
BROKER_LOG=$HACONF/broker.out
DATASET=$BASE/testing/datasets/min_6000xh_tl.json
PIDDIR=$BASE/.pids
SIM_PID_FILE=$PIDDIR/sim.pid

mkdir -p "$PIDDIR" 2>/dev/null || true

activate() {
  if [ ! -f "$VENVDIR/bin/activate" ]; then
    echo "[dev-start] Creating virtualenv at $VENVDIR";
    python -m venv "$VENVDIR";
    . "$VENVDIR/bin/activate";
    pip install --upgrade pip >/dev/null 2>&1 || true
    if [ -f /workspace/requirements_dev.txt ]; then
      pip install -r /workspace/requirements_dev.txt >/dev/null 2>&1 || true
    fi
  else
    . "$VENVDIR/bin/activate"
  fi
}


is_running() { local f=$1; [ -f "$f" ] && kill -0 "$(cat "$f" 2>/dev/null)" 2>/dev/null; }

start_simulator() {
  if is_running "$SIM_PID_FILE"; then
    echo "[dev-start] Simulator already running (PID $(cat "$SIM_PID_FILE"))"; return 0; fi
  activate
  echo "[dev-start] Starting Modbus simulator..."
  nohup python testing/modbus_simulator.py --dataset "$DATASET" & echo $! > "$SIM_PID_FILE"
  sleep 2
  if is_running "$SIM_PID_FILE"; then echo "[dev-start] Simulator started PID $(cat "$SIM_PID_FILE")"; else echo "[dev-start] Simulator failed"; fi
}

stop_proc() { local name=$1 pidfile=$2; if is_running "$pidfile"; then kill "$(cat "$pidfile")" 2>/dev/null || true; sleep 1; if is_running "$pidfile"; then kill -9 "$(cat "$pidfile")" 2>/dev/null || true; fi; rm -f "$pidfile"; echo "[dev-start] Stopped $name"; else echo "[dev-start] $name not running"; fi }

status() {
  if is_running "$SIM_PID_FILE"; then echo "Simulator: RUNNING (PID $(cat "$SIM_PID_FILE"))"; else echo "Simulator: stopped"; fi
}


case "$ACTION" in
  noop)
    echo "[dev-start] No action (explicit start required). Available: start|stop|restart|status";
    ;;
  start)
    start_simulator
    status
    ;;
  stop)
    stop_proc Simulator "$SIM_PID_FILE"
    ;;
  restart)
    "$0" stop || true
    "$0" start
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}"; exit 2;
esac

exit 0
